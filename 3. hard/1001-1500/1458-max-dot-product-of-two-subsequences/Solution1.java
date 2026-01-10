// LeetCode #1458: Max Dot Product of Two Subsequences
// Approach: [Approach Name]
// Status: ✅ Accepted
// Time: O()  |  Space: O()

class Solution {
    public int maxDotProduct(int[] nums1, int[] nums2) {
        if (nums1[0] > nums2[0]){
            int[] tmp = nums1; nums1 = nums2; nums2 = tmp;
        }
        int max1 = Arrays.stream(nums1).max().getAsInt();
        int min2 = Arrays.stream(nums2).min().getAsInt();
        if (max1 < 0 && min2 > 0)
            return max1 * min2;
        int m = nums1.length, n = nums2.length;
        int[] dp = new int[n + 1];
        for (int i = 0; i < m; i++){
            for (int j = n - 1; j >= 0; j--){
                int v = nums1[i] * nums2[j] + dp[j];
                if (v > dp[j + 1])
                    dp[j + 1] = v;
            }
            for (int j = 0; j < n; j++){
                if (dp[j + 1] < dp[j])
                    dp[j + 1] = dp[j];
            }
        }
        return dp[n];
    }
}
