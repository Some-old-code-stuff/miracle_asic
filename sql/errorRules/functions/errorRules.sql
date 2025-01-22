create or replace function error_rules(type integer default NULL )
  returns common_errorrule as $$
  select common_errorrule.*
from common_errorrule
where ($1 isnull or asic_type = $1)
ORDER BY asic_type, value_type
  $$ language sql stable;