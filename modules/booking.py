# =====================================================================
# [Member 2] 자료구조: 체이닝 해시 테이블 (Chaining Hash Table)
# 선택 이유: 방 ID를 키로 하여 강의실 상태를 O(1)만에 조회 및 업데이트하기 위함.
# =====================================================================
class RoomHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash_function(self, key):
        return sum(ord(char) for char in key) % self.size

    def insert(self, key, value):
        # # 자료구조: 해시 테이블 삽입
        hash_index = self._hash_function(key)
        for pair in self.table[hash_index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[hash_index].append([key, value])

    def search(self, key):
        # # 자료구조: 해시 테이블 검색
        hash_index = self._hash_function(key)
        for pair in self.table[hash_index]:
            if pair[0] == key:
                return pair[1]
        return None


# =====================================================================
# [Member 2] 자료구조: 이진 탐색 트리 (Binary Search Tree - BST)
# 선택 이유: 학번 기준으로 예약 내역을 정렬된 상태로 유지하고 탐색하기 위함.
# =====================================================================
class BSTNode:
    def __init__(self, student_id, room_id):
        self.student_id = student_id
        self.room_id = room_id
        self.left = None
        self.right = None

class BookingBST:
    def __init__(self):
        self.root = None

    def insert(self, student_id, room_id):
        new_node = BSTNode(student_id, room_id)
        if self.root is None:
            self.root = new_node
        else:
            self._insert_value(self.root, new_node)

    def _insert_value(self, current_node, new_node):
        if new_node.student_id < current_node.student_id:
            if current_node.left is None:
                current_node.left = new_node
            else:
                self._insert_value(current_node.left, new_node)
        else:
            if current_node.right is None:
                current_node.right = new_node
            else:
                self._insert_value(current_node.right, new_node)

    def search(self, student_id):
        return self._search_value(self.root, student_id)

    def _search_value(self, current_node, student_id):
        if current_node is None or current_node.student_id == student_id:
            return current_node
        if student_id < current_node.student_id:
            return self._search_value(current_node.left, student_id)
        return self._search_value(current_node.right, student_id)


# =====================================================================
# [Member 2] 알고리즘: 퀵 정렬 (Quick Sort)
# 선택 이유: 강의실 수용 인원 기준으로 대용량 데이터를 빠르게 정렬하기 위함.
# =====================================================================
def quick_sort_rooms(room_list):
    # # 알고리즘: 퀵 정렬
    if len(room_list) <= 1:
        return room_list
    pivot = room_list[0]
    less = [x for x in room_list[1:] if x['capacity'] <= pivot['capacity']]
    greater = [x for x in room_list[1:] if x['capacity'] > pivot['capacity']]
    return quick_sort_rooms(less) + [pivot] + quick_sort_rooms(greater)


# =====================================================================
# [Member 2] 알고리즘: 이진 탐색 (Binary Search)
# 선택 이유: 정렬된 강의실 목록에서 특정 수용 인원을 가진 방을 O(log N)으로 찾기 위함.
# =====================================================================
def binary_search_by_capacity(sorted_rooms, target_capacity):
    # # 알고리즘: 이진 탐색
    low = 0
    high = len(sorted_rooms) - 1

    while low <= high:
        mid = (low + high) // 2
        if sorted_rooms[mid]['capacity'] == target_capacity:
            return sorted_rooms[mid]
        elif sorted_rooms[mid]['capacity'] < target_capacity:
            low = mid + 1
        else:
            high = mid - 1
    return None