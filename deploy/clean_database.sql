delete from common_jsoninfo;
delete from common_asicinfo where id not in (select asic_info_id from common_asic where not asic_info_id ISNULL );
vacuum ANALYZE;
vacuum full;