CREATE OR REPLACE FUNCTION public.search_asics(
  -- @fieldName asicTypeSmth
  arg_asic_type                 INT DEFAULT NULL,
  arg_alg_type                  INT DEFAULT NULL,
  arg_farm                      INT DEFAULT NULL,
  arg_client                    INT DEFAULT NULL,
  arg_ip_address                TEXT DEFAULT NULL,
  arg_pool_status               TEXT DEFAULT NULL,
  arg_farm_name                 TEXT DEFAULT NULL,
  arg_asic_name                 TEXT DEFAULT NULL,
  arg_client_name               TEXT DEFAULT NULL,
  arg_error_level               INT DEFAULT NULL,
  arg_field_name                TEXT DEFAULT NULL,
  arg_with_disabled_auto_update BOOLEAN DEFAULT FALSE,
  arg_with_connection_errors    BOOLEAN DEFAULT FALSE,
  arg_with_errors               BOOLEAN DEFAULT FALSE,
  arg_with_warnings             BOOLEAN DEFAULT FALSE,
  arg_unregistered_asics        BOOLEAN DEFAULT FALSE
)
  RETURNS SETOF public.common_asic AS $$
WITH asic_fields AS (
    SELECT
      "common_asic"."id",
      "common_asic"."type",
      "common_asic"."crypt_type",
      "common_asic"."alg_type",
      "common_asic"."name",
      "common_asic"."ip_address",
      "common_asic"."host_name",
      "common_asic"."default_rate",
      "common_asic"."measure",
      "common_asic"."asic_name",
      "common_asic"."pool_status",
      "common_asic"."full_rate",
      "common_asic"."pool_address",
      "common_asic"."pool_username",
      "common_asic"."updated",
      "common_asic"."stop_update",
      "common_asic"."username",
      "common_asic"."password",
      "common_asic"."farm_id",
      "common_asic"."client_id",
      "common_asic"."asic_info_id",
      "common_asic"."resume_update_date",
      COALESCE(
          (SELECT COUNT(U0."id") AS "cnt"
           FROM "common_error" U0
           WHERE (U0."asic_id" = ("common_asic"."id")
                  AND U0."status" < 4
                  AND (arg_error_level IS NULL OR U0."level" = arg_error_level)
                  AND (field_name IS NULL OR U0."field_name" = arg_field_name))
           GROUP BY U0."asic_id"
           LIMIT 1), 0)      AS "error_filter_count",
      COALESCE(
          (SELECT COUNT(U0."id") AS "cnt"
           FROM "common_error" U0
           WHERE (U0."level" = 2
                  AND U0."status" < 4
                  AND U0."asic_id" = ("common_asic"."id"))
           GROUP BY U0."asic_id"
           LIMIT 1), 0)      AS "error_count",
      COALESCE(
          (SELECT COUNT(U0."id") AS "cnt"
           FROM "common_error" U0
           WHERE (U0."level" = 1
                  AND U0."status" < 4
                  AND U0."asic_id" = ("common_asic"."id"))
           GROUP BY U0."asic_id"
           LIMIT 1), 0)      AS "warning_count",
      COALESCE(
          (SELECT COUNT(U0."id") AS "cnt"
           FROM "common_error" U0
           WHERE (U0."field_name" = 'connect_error'
                  AND U0."status" < 4
                  AND U0."asic_id" = ("common_asic"."id"))
           GROUP BY U0."asic_id"
           LIMIT 1), 0)      AS "connect_problems",
      "common_farm"."name"   AS "farm_name",
      "common_client"."name" AS "client_name"
    FROM "common_asic"
      LEFT JOIN "common_farm" ON ("common_asic"."farm_id" = "common_farm"."id")
      LEFT JOIN "common_client" ON ("common_asic"."client_id" = "common_client"."id"))
SELECT
  "id",
  "type",
  "crypt_type",
  "name",
  "ip_address",
  "host_name",
  "default_rate",
  "measure",
  "alg_type",
  "farm_id",
  "client_id",
  "asic_name",
  "pool_status",
  "updated",
  "full_rate",
  "pool_address",
  "pool_username",
  "stop_update",
  "asic_info_id",
  "password",
  "username",
  "resume_update_date"
FROM asic_fields
WHERE (
  (arg_asic_type IS NULL OR "asic_fields"."type" = arg_asic_type)
  AND (arg_alg_type IS NULL OR "asic_fields"."alg_type" = arg_alg_type)
  AND (arg_farm IS NULL OR "asic_fields"."farm_id" = arg_farm)
  AND (arg_client IS NULL OR "asic_fields"."client_id" = arg_client)
  AND (arg_ip_address IS NULL OR UPPER("asic_fields"."ip_address" :: TEXT) LIKE UPPER('%' || arg_ip_address || '%'))
  AND (arg_asic_name IS NULL OR UPPER("asic_fields"."asic_name" :: TEXT) LIKE UPPER('%' || arg_asic_name || '%'))
  AND (arg_pool_status IS NULL OR UPPER("asic_fields"."pool_status" :: TEXT) LIKE UPPER('%a' || arg_pool_status || '%'))
  AND (arg_client_name IS NULL OR UPPER("asic_fields"."client_name" :: TEXT) LIKE UPPER('%' || arg_client_name || '%'))
  AND (arg_farm_name IS NULL OR UPPER("asic_fields"."farm_name" :: TEXT) LIKE UPPER('%' || arg_farm_name || '%'))
  AND (arg_error_level IS NULL OR arg_field_name IS NULL OR "error_filter_count" > 0)
  AND "asic_fields"."stop_update" = arg_with_disabled_auto_update
  AND (NOT arg_with_errors OR "error_count" > 0)
  AND (NOT arg_with_warnings OR "warning_count" > 0)
  AND (NOT arg_with_connection_errors OR "connect_problems" > 0)
  AND (NOT arg_unregistered_asics OR ("farm_id" IS NULL
                                      OR "client_id" IS NULL)))
ORDER BY "error_count" DESC,
  "warning_count" DESC

$$ LANGUAGE SQL STABLE;