import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { motion } from "framer-motion";

interface RevenueChartProps {
  data:
    | {
        order_year_month: string;
        total_revenue: number;
      }[]
    | null;
}

export default function RevenueChart({ data }: RevenueChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="glass-card rounded-2xl shadow-glow-lg p-8 border border-purple-500/20 transition-smooth hover:shadow-glow-lg">
        <h2 className="text-3xl font-bold text-white mb-4">
          💰 Monthly Revenue Trend
        </h2>
        <p className="text-purple-200">No data available</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      whileInView={{ opacity: 1, scale: 1 }}
      whileHover={{ y: -5, boxShadow: "0 0 30px rgba(139, 92, 246, 0.4)" }}
      viewport={{ once: true, amount: 0.3 }}
      transition={{ duration: 0.3 }}
      className="glass-card rounded-2xl shadow-glow-lg p-8 border border-purple-500/40 transition-smooth"
    >
      <h2 className="text-3xl font-bold text-slate-50 mb-6">
        💰 <span className="gradient-text">Monthly Revenue Trend</span>
      </h2>
      <div
        style={{ height: "350px" }}
        className="w-full rounded-xl overflow-hidden bg-slate-800/60"
      >
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="rgba(148, 163, 184, 0.3)"
            />
            <XAxis
              dataKey="order_year_month"
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
            <Line
              type="monotone"
              dataKey="total_revenue"
              stroke="url(#gradient)"
              strokeWidth={3}
              dot={{ fill: "#a8a2ff", r: 5, strokeWidth: 2, stroke: "#6366f1" }}
              activeDot={{ r: 7, strokeWidth: 2 }}
              name="Total Revenue"
            />
            <defs>
              <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#667eea" />
                <stop offset="100%" stopColor="#764ba2" />
              </linearGradient>
            </defs>
          </LineChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  );
}
