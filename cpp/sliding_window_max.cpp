/**
 * ============================================================
 * ACM-ICPC 级别算法题：滑动窗口最大值 (Sliding Window Maximum)
 * ============================================================
 *
 * 题目描述：
 * 给定一个整数数组 nums 和一个大小为 k 的滑动窗口，
 * 从数组最左侧滑到最右侧，返回每个窗口位置中的最大值。
 *
 * 输入：
 *   第一行：n k
 *   第二行：n 个整数
 * 输出：
 *   n-k+1 个整数，每个窗口的最大值
 *
 * 样例：
 *   输入：8 3
 *         1 3 -1 -3 5 3 6 7
 *   输出：3 3 5 5 6 7
 *
 * 解法：单调递减双端队列 (Monotonic Deque)
 *   时间复杂度：O(n)  —— 每个元素最多入队、出队各一次
 *   空间复杂度：O(k)
 */

#include <iostream>
#include <vector>
#include <deque>
using namespace std;

vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    deque<int> dq;          // 存下标，保持对应值单调递减
    vector<int> result;
    int n = nums.size();

    for (int i = 0; i < n; i++) {
        // 1. 弹出队尾所有比当前值小的元素
        //    （它们不可能成为当前及未来窗口的最大值）
        while (!dq.empty() && nums[dq.back()] < nums[i]) {
            dq.pop_back();
        }

        // 2. 当前下标入队
        dq.push_back(i);

        // 3. 弹出已超出窗口范围的队首元素
        if (dq.front() <= i - k) {
            dq.pop_front();
        }

        // 4. 窗口形成后，队首即为最大值
        if (i >= k - 1) {
            result.push_back(nums[dq.front()]);
        }
    }

    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;

    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];

    vector<int> ans = maxSlidingWindow(nums, k);

    for (int i = 0; i < (int)ans.size(); i++) {
        if (i) cout << " ";
        cout << ans[i];
    }
    cout << endl;

    return 0;
}
