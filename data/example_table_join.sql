SELECT * FROM events;

-- SELECT * FROM events INNER JOIN xref_event_targets ON events_id=events.rowid;

SELECT * FROM entities;

-- SELECT * FROM (
        -- events INNER JOIN xref_event_targets ON events_id=events.rowid
-- ) INNER JOIN entities ON entities.rowid=target_id;
