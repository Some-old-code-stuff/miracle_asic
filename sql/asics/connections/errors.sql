CREATE OR REPLACE FUNCTION common_asic_errors(u common_asic)
  RETURNS SETOF common_error AS $$
SELECT distinct on ("common_error"."asic_id",
                    "common_error"."field_name",
                    "common_error"."level",
                    "common_error"."object_id") common_error.*
FROM common_error
WHERE common_error.status < 4
      AND common_error.asic_id = u.id
ORDER BY "common_error"."asic_id" ASC,
         "common_error"."field_name" ASC,
         "common_error"."level" ASC,
         "common_error"."object_id" ASC,
         "common_error"."created" DESC
$$ LANGUAGE SQL STABLE;

comment on FUNCTION common_asic_errors(common_asic) is  E'@foreignFieldName errors\n @fieldName errors';