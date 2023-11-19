PRAGMA foreign_keys = false;

CREATE TABLE IF NOT EXISTS "peers" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "uid" integer,
  "client_id" text(255),
  "username" text(255),
  "hostname" text(255),
  "alias" text(255),
  "platform" text(255),
  "tags" text(255),
  "forceAlwaysRelay" text(255),
  "rdpPort" text(255),
  "rdpUsername" text(255)
);

CREATE TABLE IF NOT EXISTS "system_info" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "client_id" text(255),
  "hostname" text(255),
  "cpu" text(255),
  "memory" text(255),
  "os" text(255),
  "uuid" text(255),
  "version" text(255)
);


CREATE TABLE IF NOT EXISTS "tags" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "uid" integer,
  "tag" text(255)
);

CREATE TABLE IF NOT EXISTS "token" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "username" text(255),
  "uid" integer,
  "client_id" text(255),
  "uuid" text(255),
  "access_token" text(255),
  "create_time" text(255)
);

CREATE TABLE IF NOT EXISTS "users" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "username" text(255),
  "password" text(255),
  "email" text(255),
  "note" text(255),
  "status" integer,
  "group" text(255),
  "is_admin" integer,
  "create_time" text(255),
  "update_time" text(255)
);

CREATE UNIQUE INDEX IF NOT EXISTS "uid"
ON "token" (
  "uid" ASC,
  "client_id" ASC,
  "uuid" ASC
);

CREATE UNIQUE INDEX IF NOT EXISTS "username"
ON "users" (
  "username" ASC
);

PRAGMA foreign_keys = true;
