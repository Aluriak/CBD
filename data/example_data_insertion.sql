-- Row readed in event file is:

-------------------------------------------------
-- SourceId	SourceLabel	SourceEntityType	EdgeLabel	TargetId
-- 10090	mouse	        S	                co-occurrence   P81172


-- TargetLabel	TargetEntityType	PUBMED_ID	nsent	ntagged_nsent	nsent_nrelation	period
-- Hepcidin	P	                11113132	1	1	        1	        2001-03-01
-------------------------------------------------
-- NB: real value for TargetId is a list of targets id like P81172;P82951;Q5NVR8;Q5U9D2;Q8MJ80;Q99MH3;Q9DFD6;Q9EQ21

-- this file describes the queries needed for include this row in database (assumed already created).
-- fields nsent, ntagged_nsent and nsent_nrelation are unused.

-- ENTITY INSERTION
INSERT INTO entities
     -- SourceId, SourceLabel, type_id
VALUES ('10090' , 'mouse'    , (SELECT rowid FROM types WHERE label = 'S'));

-- PUBMED_ID: csv database is ok for all pubmed ids. (all match '[0-9]{8}')
INSERT OR IGNORE INTO publications VALUES (11113132);

-- EVENTS INSERTION
INSERT INTO events VALUES (
        (SELECT rowid FROM entities WHERE db_id = '10090'),            -- source rowid in entities
        (SELECT rowid FROM entities WHERE db_id = 'P81172'),           -- target rowid in entities
        (SELECT rowid FROM publications WHERE pubmed_id = 11113132), -- targeted rowid in publications
        'co-occurrence',
        2001 -- year of discovering
);

-- XREF INSERTION: must be performed for each TargetId
INSERT INTO xref_event_targets VALUES (
        (SELECT MAX(rowid) FROM events), -- last inserted rowid in events
        'P81172' -- first target id. 
);

