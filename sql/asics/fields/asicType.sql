CREATE OR REPLACE FUNCTION common_asic_asic_type(u common_asic)
  RETURNS VARCHAR AS $$
SELECT convert_asic_type(u.type)
$$ LANGUAGE SQL STABLE;

COMMENT ON FUNCTION common_asic_asic_type(common_asic) IS
E'@fieldName type';
COMMENT ON COLUMN common_asic.type IS E'@name type_value';