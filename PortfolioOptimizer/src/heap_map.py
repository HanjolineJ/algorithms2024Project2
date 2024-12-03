import numpy as np
import os
import matplotlib.pyplot as plt
import heapq
import squarify  # Install this with `pip install squarify`


class HeapMap:
    def __init__(self, portfolio_values, asset_names):
        if portfolio_values.ndim != 3:
            raise ValueError(f"Expected a 3D array for portfolio_values, got {portfolio_values.ndim}D")
        if len(asset_names) != portfolio_values.shape[2]:
            raise ValueError("Asset names must match the last dimension of portfolio_values.")
        self.portfolio_values = portfolio_values
        self.asset_names = asset_names

    def calculate_asset_risks(self):
        asset_values = self.portfolio_values.transpose(2, 0, 1)
        risks = []

        for i, asset in enumerate(self.asset_names):
            daily_returns = np.diff(asset_values[i], axis=0) / asset_values[i][:-1]
            risk = np.std(daily_returns) + np.abs(np.mean(daily_returns))  # Combines volatility and average return
            risks.append((risk, asset))

        return risks

    def generate_heap(self):
        """Generate a heap based on asset risks."""
        asset_risks = self.calculate_asset_risks()
        max_heap = [(-risk, asset) for risk, asset in asset_risks]
        heapq.heapify(max_heap)
        return max_heap

    def display_heap(self, heap):
        print("Heap Map: Areas of Higher Portfolio Risk")
        print("-" * 50)
        for neg_risk, asset in heap:
            print(f"Asset: {asset}, Risk: {-neg_risk:.4f}")

    def export_treemap(self, heap, filename="heap_treemap.png"):
        """
        Exports a treemap visualization of the heap.
        """
        os.makedirs("graphs", exist_ok=True)
        filepath = os.path.join("graphs", filename)

        # Extract data from the heap
        risks = [-risk for risk, asset in heap]
        assets = [asset for risk, asset in heap]

        # Normalize risks for treemap sizing
        total_risk = sum(risks)
        sizes = [risk / total_risk for risk in risks]

        # Plot treemap
        plt.figure(figsize=(10, 6))
        squarify.plot(
            sizes=sizes,
            label=[f"{asset}\nRisk: {risk:.4f}" for asset, risk in zip(assets, risks)],
            color=plt.cm.viridis(sizes),  # Color based on size
            alpha=0.7
        )
        plt.axis("off")
        plt.title("Asset Risks Treemap", fontsize=18)
        plt.savefig(filepath)
        print(f"Treemap graph saved as {filepath}")
        plt.show()
