CREATE TABLE feeds (
    id              SERIAL      PRIMARY KEY,
    feed_title      TEXT        NOT NULL,
    post_title      TEXT        NOT NULL,
    url             TEXT        NOT NULL,
    published       TEXT        NOT NULL,
    added           TIMESTAMP   DEFAULT now()
);
