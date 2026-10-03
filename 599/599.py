from collections import defaultdict
class Solution:
    def dict_index(self, arr:list) -> dict:
        result = {}
        for i, val in enumerate(arr):
            result[val] = i
        return result

    def findRestaurant(self, list1: List[str], list2: List[str]) -> List[str]:
        dict1 = self.dict_index(list1)
        ans = defaultdict(list)
        for idx, val in enumerate(list2):
            if val in dict1:
                indice = idx+dict1[val]
                ans[indice].append(val)
        min_sum = min(ans.keys())
        return ans[min_sum]
