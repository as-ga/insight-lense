import { useState } from "react";
import { motion } from "framer-motion";

interface Customer {
  name: string;
  region: string;
  total_spend: number;
  churned: boolean;
}

interface TopCustomersTableProps {
  data: Customer[] | null;
}

export default function TopCustomersTable({ data }: TopCustomersTableProps) {
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [sortConfig, setSortConfig] = useState<{
    key: keyof Customer;
    direction: "asc" | "desc";
  }>({ key: "total_spend", direction: "desc" });

  const filteredCustomers =
    data
      ?.filter(
        (c) =>
          c.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          c.region?.toLowerCase().includes(searchTerm.toLowerCase())
      )
      .sort((a, b) => {
        const aVal = a[sortConfig.key];
        const bVal = b[sortConfig.key];
        const mult = sortConfig.direction === "asc" ? 1 : -1;
        if (typeof aVal === "string")
          return mult * (aVal as string).localeCompare(bVal as string);
        return mult * ((aVal as number) - (bVal as number));
      }) || [];

  const handleSort = (key: keyof Customer) => {
    setSortConfig((prev) => ({
      key,
      direction: prev.key === key && prev.direction === "desc" ? "asc" : "desc",
    }));
  };

  if (!data || data.length === 0) {
    return (
      <div className="glass-card rounded-2xl shadow-glow-lg p-8 border border-purple-500/20 transition-smooth hover:shadow-glow-lg">
        <h2 className="text-3xl font-bold text-white mb-4">⭐ Top Customers</h2>
        <p className="text-purple-200">No data available</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      whileHover={{ y: -5, boxShadow: "0 0 30px rgba(139, 92, 246, 0.4)" }}
      viewport={{ once: true, amount: 0.3 }}
      transition={{ duration: 0.3 }}
      className="glass-card rounded-2xl shadow-glow-lg p-8 border border-purple-500/40 transition-smooth"
    >
      <h2 className="text-3xl font-bold text-slate-50 mb-6">
        ⭐ <span className="gradient-text">Top Customers</span>
      </h2>
      <div className="mb-6">
        <input
          type="text"
          placeholder="🔍 Search by name or region..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-3 border border-purple-500/50 rounded-xl bg-slate-800/80 text-slate-50 placeholder-slate-400 focus:ring-2 focus:ring-purple-500/80 focus:border-purple-500/60 transition-smooth backdrop-blur"
        />
      </div>
      {filteredCustomers.length > 0 ? (
        <div className="overflow-x-auto rounded-xl border border-purple-500/40">
          <table className="w-full">
            <thead className="bg-slate-700/80 border-b border-purple-500/40">
              <tr>
                <th
                  onClick={() => handleSort("name")}
                  className="px-4 py-4 text-left cursor-pointer hover:bg-slate-600/80 font-semibold text-slate-50 transition-smooth"
                >
                  Name{" "}
                  {sortConfig.key === "name" && (
                    <span className="text-xs">
                      {sortConfig.direction === "asc" ? "↑" : "↓"}
                    </span>
                  )}
                </th>
                <th
                  onClick={() => handleSort("region")}
                  className="px-4 py-4 text-left cursor-pointer hover:bg-slate-600/80 font-semibold text-slate-50 transition-smooth"
                >
                  Region{" "}
                  {sortConfig.key === "region" && (
                    <span className="text-xs">
                      {sortConfig.direction === "asc" ? "↑" : "↓"}
                    </span>
                  )}
                </th>
                <th
                  onClick={() => handleSort("total_spend")}
                  className="px-4 py-4 text-left cursor-pointer hover:bg-slate-600/80 font-semibold text-slate-50 transition-smooth"
                >
                  Total Spend{" "}
                  {sortConfig.key === "total_spend" && (
                    <span className="text-xs">
                      {sortConfig.direction === "asc" ? "↑" : "↓"}
                    </span>
                  )}
                </th>
                <th
                  onClick={() => handleSort("churned")}
                  className="px-4 py-4 text-left cursor-pointer hover:bg-slate-600/80 font-semibold text-slate-50 transition-smooth"
                >
                  Status{" "}
                  {sortConfig.key === "churned" && (
                    <span className="text-xs">
                      {sortConfig.direction === "asc" ? "↑" : "↓"}
                    </span>
                  )}
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredCustomers.map((customer, idx) => (
                <tr
                  key={idx}
                  className={
                    idx % 2 === 0
                      ? "bg-slate-600/40 border-b border-purple-500/40 hover:bg-slate-600/60"
                      : "bg-slate-700/50 border-b border-purple-500/40 hover:bg-slate-700/70"
                  }
                >
                  <td className="px-4 py-4 text-slate-50 font-medium group-hover:text-purple-200 transition-smooth">
                    {customer.name}
                  </td>
                  <td className="px-4 py-4 text-slate-200">
                    {customer.region}
                  </td>
                  <td className="px-4 py-4 font-bold text-green-300">
                    ₹{customer.total_spend?.toFixed(2) || "0.00"}
                  </td>
                  <td className="px-4 py-4">
                    {customer.churned ? (
                      <span className="inline-block px-3 py-1 bg-red-600/60 text-red-100 rounded-full text-xs font-semibold border border-red-500/70">
                        ⚠️ Churned
                      </span>
                    ) : (
                      <span className="inline-block px-3 py-1 bg-green-600/60 text-green-100 rounded-full text-xs font-semibold border border-green-500/70">
                        ✓ Active
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="text-center py-8 text-slate-300">
          No customers found matching your search
        </div>
      )}
    </motion.div>
  );
}
