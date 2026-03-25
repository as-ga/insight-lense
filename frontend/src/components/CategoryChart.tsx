import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { motion } from "framer-motion";

interface CategoryData {
  category: string;
  total_revenue: number;
}

interface CategoryChartProps {
  data: CategoryData[] | null;
}

export default function CategoryChart({ data }: CategoryChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="glass-card rounded-2xl shadow-glow-lg p-8 border border-purple-500/20 transition-smooth hover:shadow-glow-lg">
        <h2 className="text-3xl font-bold text-white mb-4">
          📦 Category Performance
        </h2>
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
        📦 <span className="gradient-text">Category Performance</span>
      </h2>
      <div
        style={{ height: "300px" }}
        className="w-full rounded-xl overflow-hidden bg-slate-800/60"
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 20, right: 30, left: 0, bottom: 60 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="rgba(148, 163, 184, 0.3)"
            />
            <XAxis
              dataKey="category"
              angle={-45}
              textAnchor="end"
              height={80}
              stroke="rgba(203, 213, 225, 1)"
              style={{ fontSize: "12px", fill: "#cbd5e1" }}
            />
            <YAxis
              stroke="rgba(203, 213, 225, 1)"
              style={{ fontSize: "12px", fill: "#cbd5e1" }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(8, 15, 30, 0.98)",
                border: "1px solid rgba(168, 162, 255, 0.5)",
                borderRadius: "0.75rem",
                boxShadow: "0 0 20px rgba(139, 92, 246, 0.4)",
              }}
              formatter={(value) => `₹${(value as number).toFixed(2)}`}
              labelStyle={{ color: "#f1f5f9", fontWeight: "bold" }}
            />
            <Legend wrapperStyle={{ color: "#cbd5e1", fontSize: "14px" }} />
            <Bar
              dataKey="total_revenue"
              fill="url(#barGradient)"
              name="Total Revenue"
              radius={[12, 12, 0, 0]}
            />
            <defs>
              <linearGradient
                id="barGradient"
                x1="0%"
                y1="0%"
                x2="0%"
                y2="100%"
              >
                <stop offset="0%" stopColor="#667eea" />
                <stop offset="100%" stopColor="#764ba2" />
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  );
}
