def print_env_info(project_name, project_port, environment, debug, log_level, mongo_db):
    # leave as print.  This is startup env info only and doesn't need to fill the log.
    print('---------------------------------------')
    print(f'project    : {project_name} | http://localhost:{project_port}/')
    print(f'docs       : http://localhost:{project_port}/docs | http://localhost:{project_port}/redoc')
    print(f'environment: {environment} | debug: {debug} | log_level: {log_level}')
    print(f'database   : {mongo_db}')
    print('---------------------------------------')
