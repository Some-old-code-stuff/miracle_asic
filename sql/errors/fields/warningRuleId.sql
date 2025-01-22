CREATE OR REPLACE FUNCTION common_error_warning_rule_id(u common_error)
  RETURNS INT AS $$
  select common_errorrule.error_rule_id
    from common_errorrule
    where common_errorrule.id = u.error_rule_id
$$ LANGUAGE SQL STABLE;