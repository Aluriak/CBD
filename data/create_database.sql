DROP TABLE IF EXISTS types;
DROP TABLE IF EXISTS publications;
DROP TABLE IF EXISTS entities;
DROP TABLE IF EXISTS events;

-- type describes a type of entity, in (Protein P, Cell C, Tissue T, Drug D, Species S, Disease I)
CREATE TABLE types (
        t_label CHAR UNIQUE NOT NULL
);

-- a publication is about a reaction
CREATE TABLE publications (
        pubmed_id VARCHAR(127) UNIQUE NOT NULL
);

-- an entity can be anything with a swisspro id
CREATE TABLE entities (
        db_id   INTEGER      UNIQUE NOT NULL,
        e_label VARCHAR(127) NOT NULL,
        type_id INT          NOT NULL CONSTRAINT FK_types REFERENCES 'types'(rowid)
);

-- events, that are the main thing studied
CREATE TABLE events (
        source_id INT NOT NULL CONSTRAINT FK_entities REFERENCES 'entities'(rowid),
        target_id INT NOT NULL CONSTRAINT FK_entities REFERENCES 'entities'(rowid),
        publtn_id INT NOT NULL CONSTRAINT FK_publications REFERENCES 'publications'(rowid),
        edge_label VARCHAR(127) NOT NULL, -- could be a table if csv database was not so dirty
        year INT NOT NULL 
);

-- Initialize some tables that have few possible values
INSERT INTO types VALUES ('P'), ('C'), ('T'), ('D'), ('S'), ('I');

