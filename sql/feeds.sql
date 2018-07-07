CREATE TABLE IF NOT EXISTS feeds (
    id              SERIAL      PRIMARY KEY DEFAULT nextval('id_seq'),
    feed_title      TEXT        NOT NULL,
    post_title      TEXT        NOT NULL,
    url             TEXT        NOT NULL,
    published       TEXT        NOT NULL,
    added           TIMESTAMP   DEFAULT now()
);
