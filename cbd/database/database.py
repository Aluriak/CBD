# -*- coding: utf-8 -*-
#########################
#       DATABASE        #
#########################


#########################
# IMPORTS               #
#########################
from collections import defaultdict
import itertools
import sqlite3
import glob
import csv
import re




#########################
# PRE-DECLARATIONS      #
#########################
DATABASE_NAME = 'data/events.db'
EVENTS_FILE_FIELDS = (      # This is the keys (columns names)
    'SourceId',             # expected to be in events_20??.txt files
    'SourceLabel',          # Without these fields, Database object will crash.
    'SourceEntityType',
    'EdgeLabel',
    'TargetId',
    'TargetLabel',
    'TargetEntityType',
    'PUBMED_ID',
    'nsent',            # unused 
    'ntagged_nsent',    # unused
    'nsent_nrelation',  # unused
    'period',           # unused
)

YEAR_REGEX = re.compile('events_(20[01][0-9]).txt')




#########################
# CLASS                 #
#########################
class Database():
    """
    Big wrapper around using and querying SQLite database.
    Provides facilities for update and asking against the database.
    """

# CONSTRUCTOR #################################################################
    def __init__(self, repertory_glob, tables_creation_file, database_name=DATABASE_NAME, *, db_available=False):
        """Wait for a globbable list of files that contains events descriptions,
        the SQLite script that create tables, and the database name (will be used for
        save it)."""
        # create tools for access to database
        self.db_connection = sqlite3.connect(database_name)
        self.cursor = self.db_connection.cursor()
        # update with given files
        if not db_available:
            self.update(repertory_glob, tables_creation_file, database_name)


# PUBLIC METHODS ##############################################################
    def update(self, repertory_glob, tables_creation_file, database_name):
        """Update database by reading files in given globbable repertory.
        Example of valid repertory_glob: './data/*.txt'
        Example of invalid repertory_glob: './data/'
        """
        print('CREATING DATABASE…')
        print('INITIALIZATION…')
        self._init_tables(tables_creation_file, database_name)
        for filename in glob.glob(repertory_glob):
            year = int(YEAR_REGEX.findall(filename)[0])
            print('\tYEAR:', year)
            with open(filename, 'r') as fd:
                reader = csv.DictReader(fd, delimiter='\t')
                for mapped_line in reader:
                    self._insert_event_from(mapped_line, year)
        self.db_connection.commit()
        print('DONE !')

    def interaction_with(self, entity_name):
        """
        Return a generator of entity that interact with 
        entity of given name.
        """
        return itertools.chain(
            (tuplet[5] for tuplet in self.cursor.execute(
                """
                SELECT * FROM 
                    (events INNER JOIN entities 
                    ON events.target_id=entities.rowid) INNER JOIN types
                    ON entities.type_id=types.rowid
                WHERE e_label = ? AND t_label = ?
                """, 
                (entity_name, 'P')
            )), 
            (tuplet[6] for tuplet in self.cursor.execute(
                """
                SELECT * FROM 
                    (events INNER JOIN entities 
                    ON events.source_id=entities.rowid) INNER JOIN types
                    ON entities.type_id=types.rowid
                WHERE e_label = ? AND t_label = ?
                """, 
                (entity_name, 'P')
            )), 
        )

    def by_year_interaction(self, entity_name):
        """
        Return a generator of (year, count) that describes the 
        number of events that involves given entity by year.
        """
        return self.cursor.execute(
                """
                SELECT year, COUNT(*) FROM 
                    events INNER JOIN entities 
                    ON events.source_id=entities.rowid OR events.target_id=entities.rowid
                WHERE e_label = ?
                GROUP BY year
                """, 
                (entity_name,)
        )


    def associations_in_year(self, protein_name, year, *, associated_with=None, 
                            name_only=False, unique=False):
        """
        Return a generator of (db_id, label) of entities of associated_with type
        that are target of an event that have a protein with given protein_name 
        as source, for given year.
        Can also return a set of unique (db_id, label), or just the labels. 
        """
        generator = self.cursor.execute(
                """
                SELECT """+('' if name_only else 'db_id, ')+"""e_label FROM 
                    (events INNER JOIN entities 
                    ON events.target_id=entities.rowid) INNER JOIN types
                    ON entities.type_id=types.rowid
                WHERE """ + ('' if associated_with is None else 't_label = ? AND ') + """year = ?
                AND source_id IN (
                    SELECT rowid FROM entities  
                    WHERE e_label=?
                )
                """, 
                ((                  year, protein_name) if associated_with is None else 
                 ( associated_with, year, protein_name) 
                )
        )
        if name_only: generator = (_[0] for _ in generator)
        return set(generator) if unique else generator 

    def background_associations(self, protein_name, *, associated_with=None):
        """
        Return a set of label of entities of associated_with type
        that are target in a background event that have a protein with given protein_name 
        as source.
        """
        know_associations = set()
        background_associations = set()
        for year in self.years:
            associations = self.associations_in_year(protein_name, year, 
                                                     associated_with=associated_with,
                                                     name_only=True, unique=True
                                                    )
            for association in associations:
                if association in know_associations:
                    background_associations.add(association)
                else:
                    know_associations.add(association) 
        return background_associations


    def count_association_by_year(self, entity_name):
        """
        Return a nested dict like year:(entity name:count), where count 
        is the number of times the entity_name was associated with entity 
        of given entity_name for the considered year.
        """
        counters = {y:defaultdict(int) for y in self.years}
        for year, counter in counters.items():
            for entity in self.associations_in_year(entity_name, year, associated_with='P', name_only=True):
                counter[entity] += 1
        return counters

    def count_association_over_year(self, entity_name, *, minimal_count=1, unique=True):
        """
        Return a nested dict like entity name:count, where count 
        is the number of times the entity_name was associated with entity 
        of given entity_name in database.
        """
        from collections import defaultdict
        counters = defaultdict(int)
        for year in self.years:
            for entity in self.associations_in_year(entity_name, year, 
                                                    associated_with='P', 
                                                    name_only=True, 
                                                    unique=unique):
                counters[entity] += 1
        # return only those that appears at least minimal_count times
        return {k:v for k,v in counters.items() if v > minimal_count}



# PRIVATE METHODS #############################################################
    def _init_tables(self, tables_creation_file, database_name):
        """
        Create a database named database_name, by reading and executing
        content of SQL file given through tables_creation_file.
        """
        with open(tables_creation_file, 'r') as fd:
            self.cursor.executescript(fd.read())

    def _insert_event_from(self, mapped_line, year):
        """Inserts values of mapped_line """
        # all fields must be in expected list of fields
        assert(all(k in EVENTS_FILE_FIELDS for k in mapped_line.keys()))
        # translations
        mapped_line['SourceLabel'] = mapped_line['SourceLabel'].lower()
        mapped_line['TargetLabel'] = mapped_line['TargetLabel'].lower()

        # PUBLICATION INSERTION
        assert(len(mapped_line['PUBMED_ID']) == 8)
        self.cursor.execute("INSERT OR IGNORE INTO publications VALUES (?)", 
                            (mapped_line['PUBMED_ID'],)
        )

        # ENTITIES INSERTION (source & target)
        self._insert_entity(
             mapped_line['SourceId'], mapped_line['SourceLabel'], 
             mapped_line['SourceEntityType']
        )
        self._insert_entity(
             mapped_line['TargetId'], mapped_line['TargetLabel'], 
             mapped_line['TargetEntityType']
        )

        # EVENT INSERTION
        self.cursor.execute(
            """INSERT INTO events VALUES (
                    (SELECT rowid FROM entities WHERE db_id = ?),         -- source rowid in entities
                    (SELECT rowid FROM entities WHERE db_id = ?),         -- target rowid in entities
                    (SELECT rowid FROM publications WHERE pubmed_id = ?), -- targeted rowid in publications
                    ?, -- edge label
                    ?  -- year
            );""", (mapped_line['SourceId'] , mapped_line['TargetId'] , 
                    mapped_line['PUBMED_ID'], mapped_line['EdgeLabel'], year)
        );



# CLASS METHODS ###############################################################
# PRIVATE METHODS #############################################################
    def _insert_entity(self, source_id, source_label, source_entity_type):
        """Insert given data in table entities. If already inserted, 
        no modification performed."""
        self.cursor.execute(
            """
            INSERT OR IGNORE INTO entities VALUES 
            (? , ? , (SELECT rowid FROM types WHERE t_label = ?));
            """,
            (source_id, source_label, source_entity_type)
        );

# PREDICATS ###################################################################
# ACCESSORS ###################################################################
    @property
    def years(self):
        return sorted(tuple(_[0] for _ in self.cursor.execute("""SELECT DISTINCT year FROM events""")))
# CONVERSION ##################################################################
# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################



