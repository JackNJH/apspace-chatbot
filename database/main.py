from initialization import initialize_database
from data_insertion import insert_sample_data
from data_query import get_next_class, get_all_classes, clear_all_data, get_all_classes_today

def main():
    # initialize_database()
    # insert_sample_data()

    next_class = get_next_class()
    all_classes = get_all_classes()
    all_classes_today = get_all_classes_today()

    print("Next Class:", next_class)
    print("All Classes:", all_classes)
    print("All Classes Today:", all_classes_today)

main()
# clear_all_data()