CREATE OR REPLACE FUNCTION public.dashboard_asics()
  RETURNS SETOF public.common_asic AS $$
WITH asic_fields as (SELECT
        "common_asic".*,
        COALESCE(
            (SELECT COUNT(U0."id") AS "cnt"
             FROM "common_error" U0
             WHERE (U0."level" = 2
                    AND U0."status" < 4
                    AND U0."asic_id" = ("common_asic"."id"))
             GROUP BY U0."asic_id"
             LIMIT 1), 0) AS "error_count",
        COALESCE(
            (SELECT COUNT(U0."id") AS "cnt"
             FROM "common_error" U0
             WHERE (U0."level" = 1
                    AND U0."status" < 4
                    AND U0."asic_id" = ("common_asic"."id"))
             GROUP BY U0."asic_id"
             LIMIT 1), 0) AS "warning_count",
        COALESCE(
            (SELECT COUNT(U0."id") AS "cnt"
             FROM "common_error" U0
             WHERE (U0."field_name" = 'connect_error'
                    AND U0."status" < 4
                    AND U0."asic_id" = ("common_asic"."id"))
             GROUP BY U0."asic_id"
             LIMIT 1), 0) AS "connect_problems"
      FROM "common_asic"
      WHERE (COALESCE(
                 (SELECT COUNT(U0."id") AS "cnt"
                  FROM "common_error" U0
                  WHERE (U0."level" = 2
                         AND U0."status" < 4
                         AND U0."asic_id" = ("common_asic"."id"))
                  GROUP BY U0."asic_id"
                  LIMIT 1), 0) > 0
             AND COALESCE(
                     (SELECT COUNT(U0."id") AS "cnt"
                      FROM "common_error" U0
                      WHERE (U0."field_name" = 'connect_error'
                             AND U0."status" < 4
                             AND U0."asic_id" = ("common_asic"."id"))
                      GROUP BY U0."asic_id"
                      LIMIT 1), 0) = 0)
      ORDER BY "error_count" DESC,
        "warning_count" DESC)
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
FROM asic_fields;

$$ LANGUAGE SQL STABLE;