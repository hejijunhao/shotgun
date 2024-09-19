class Table:
    all_tables = {}  # Class variable to store all table instances

    def __init__(self, id, capacity, mergable=False):
        self.id = id
        self.capacity = capacity
        self.mergable = mergable
        self.merged_with = None
        Table.all_tables[id] = self  # Add this table to the class-wide dictionary

    def merge_with(self, other_table):
        if self.mergable and other_table.mergable and not self.merged_with and not other_table.merged_with:
            self.merged_with = other_table.id
            other_table.merged_with = self.id
            return True
        return False

    def unmerge(self):
        if self.merged_with:
            other_table = Table.get_table_by_id(self.merged_with)
            if other_table:
                other_table.merged_with = None
            self.merged_with = None
            return True
        return False

    def is_available(self):
        return not self.merged_with

    def get_effective_capacity(self):
        if self.merged_with:
            other_table = Table.get_table_by_id(self.merged_with)
            return self.capacity + (other_table.capacity if other_table else 0)
        return self.capacity

    def can_accommodate(self, party_size):
        return party_size <= self.get_effective_capacity()

    @staticmethod
    def get_table_by_id(table_id):
        return Table.all_tables.get(table_id)

    def __str__(self):
        status = "Merged" if self.merged_with else "Available"
        return f"Table {self.id}: Capacity {self.get_effective_capacity()}, {status}, {'Mergable' if self.mergable else 'Not Mergable'}"