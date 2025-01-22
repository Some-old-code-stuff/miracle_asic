CREATE or replace FUNCTION common_asic_updated(u common_asic)
  RETURNS VARCHAR AS $$
  SELECT
    CASE
      when u.updated ISNULL then 'Не обновлялся'
    ELSE
      to_char(u.updated, 'DD.MM HH24:MI:SS')
    END
$$ LANGUAGE SQL STABLE;

comment on function common_asic_updated(common_asic) is
  E'@fieldName updated';
comment on column common_asic.updated is E'@name updated_value';