--
-- File generated with SQLiteStudio v3.2.1 on Fri Dec 27 13:10:06 2019
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: douban_movie_info
DROP TABLE IF EXISTS douban_movie_info;

CREATE TABLE douban_movie_info (
    id             INTEGER        PRIMARY KEY AUTOINCREMENT,
    movie_id       INTEGER        NOT NULL
                                  UNIQUE ON CONFLICT ROLLBACK,
    title          VARCHAR (1024),
    cover          VARCHAR (1024),
    director       VARCHAR (1024),
    scriptwriter   VARCHAR (1024),
    starring       VARCHAR (2048),
    movie_type     VARCHAR (1024),
    region         VARCHAR (1024),
    language       VARCHAR (1024),
    release_date   VARCHAR (1024),
    running_time   VARCHAR (1024),
    alternate_name VARCHAR (1024),
    imdb           VARCHAR (1024),
    rating         INTEGER,
    rating_people  BIGINT,
    created_time   DATETIME,
    updated_time   DATETIME
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
