def get_config_header(project_name: str):
    return (
        f"#define {project_name}_VERSION_MAJOR 1\n"
        f"#define {project_name}_VERSION_MINOR 0"
    )


def get_header(project_name: str, file_name: str):
    return (
        f"#ifndef {project_name.upper()}_{file_name.upper()}_H\n"
        f"#define {project_name.upper()}_{file_name.upper()}_H\n"
        f"\n"
        f"\n"
        f"#endif //{project_name.upper()}_{file_name.upper()}_H\n"
    )
