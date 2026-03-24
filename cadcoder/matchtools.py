def match_key_startswith(matrix_ky_startswith: list, tuple_key_string: tuple) -> bool:
    for k, sw in matrix_ky_startswith:
        if tuple_key_string[0] == k and tuple_key_string[1].startswith(sw):
            return True
    return False


def main():
    test_matrix = [
        # seen these in PartDesign Body. we don't need them because they are auto-created with new Body.
        # TypeId, Name Prefix
        ('App::Line', 'X_Axis'),
        ('App::Line', 'Y_Axis'),
        ('App::Line', 'Z_Axis'),
        ('App::Plane', 'XY_Plane'),
        ('App::Plane', 'XZ_Plane'),
        ('App::Plane', 'YZ_Plane'),
        ('App::Origin', 'Origin'),
    ]

    test_keys = [
        ('App::Line', 'X_Axis'),
        ('App::Line', 'X_Axis001'),
        ('App::Box', 'Box'),  # should not match
        ('App::Box', 'Box001'),  # should not match
    ]

    for key in test_keys:
        if match_key_startswith(test_matrix, key):
            print(f"Matched: {key}")
        else:
            print(f"Not matched: {key}")

if __name__ == "__main__":
    main()
