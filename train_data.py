TRAIN_DATA = [
    # ("exit", {"entities": [(0, 4, "ACTION")]}),
    ("create a meeting on 12.2.2019 9:00AM for fuseday at tikal",
     {"entities": [(0, 6, "ACTION"),
                   (20, 36, "DATE"),
                   (41, 48, "PURPOSE"),
                   (52, 57, "LOCATION")]}),
    ("delete a meeting on 30.3.2019 10:00PM",
     {"entities": [(0, 6, "ACTION"),
                   (20, 37, "DATE")]}),
    ("set an appointment for miri review on 12.2.2019 11:00AM at the office",
     {"entities": [(0, 3, "ACTION"),
                   (23, 34, "PURPOSE"),
                   (38, 55, "DATE"),
                   (59, 69, "LOCATION")]}),
    ("book a meeting for code review in two days at Rabin square",
     {"entities": [(0, 4, "ACTION"),
                   (16, 31, "PURPOSE"),
                   (32, 43, "DATE"),
                   (53, 65, "LOCATION")]}),
    ("book a meeting for code review in two weeks at Rabin square",
     {"entities": [(0, 4, "ACTION"),
                   (16, 31, "PURPOSE"),
                   (32, 44, "DATE"),
                   (54, 66, "LOCATION")]}),
    ("book a meeting for code review in two years at Rabin square",
     {"entities": [(0, 4, "ACTION"),
                   (16, 31, "PURPOSE"),
                   (32, 44, "DATE"),
                   (54, 66, "LOCATION")]}),
    ("show one events",
     {"entities": [(0, 4, "ACTION"),
                   (5, 8, "NUM_TO_SHOW")]}),
    ("display two events",
     {"entities": [(0, 7, "ACTION"),
                   (8, 11, "NUM_TO_SHOW")]}),
]

