def get_config_header(project_name: str):
    return (
        f'#define {project_name}_VERSION_MAJOR 1\n'
        f'#define {project_name}_VERSION_MINOR 0'
    )
