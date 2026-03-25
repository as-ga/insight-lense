import { motion } from "framer-motion";

interface RegionalData {
  region: string;
  num_customers: number;
  num_orders: number;
  total_revenue: number;
  avg_revenue_per_customer: number;
}

interface RegionalCardsProps {
  data: RegionalData[] | null;
}

export default function RegionalCards({ data }: RegionalCardsProps) {
  if (!data || data.length === 0) {
    return (
      <div className="glass-card rounded-2xl shadow-glow-lg p-8 border border-purple-500/20 transition-smooth hover:shadow-glow-lg">
        <h2 className="text-3xl font-bold text-white mb-4">
          🌍 Regional Analysis
        </h2>
        <p className="text-purple-200">No data available</p>
      </div>
    );
  }

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.3 } },
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      whileHover={{ y: -5 }}
      viewport={{ once: true, amount: 0.3 }}
      transition={{ duration: 0.3 }}
      className="glass-card rounded-2xl shadow-glow-lg p-8 border border-purple-500/40 transition-smooth"
    >
      <h2 className="text-3xl font-bold text-slate-50 mb-6">
        🌍 <span className="gradient-text">Regional Analysis</span>
      </h2>
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 gap-4"
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.3 }}
      >
        {data.map((region, i) => (
          <motion.div
            key={i}
            variants={itemVariants}
            className="group bg-slate-700/80 rounded-xl p-6 border border-purple-400/50 transition-smooth hover:border-purple-400/80 hover:shadow-glow cursor-pointer"
          >
            <h3 className="text-xl font-bold text-slate-50 mb-4 group-hover:text-purple-100 transition-smooth">
              {region.region}
            </h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between group-hover:translate-x-1 transition-smooth duration-300">
                <span className="text-slate-200 text-sm font-medium">
                  👥 Customers:
                </span>
                <strong className="text-slate-50 text-lg font-bold">
                  {Math.round(region.num_customers)}
                </strong>
              </div>
              <div className="flex items-center justify-between group-hover:translate-x-1 transition-smooth duration-300">
                <span className="text-slate-200 text-sm font-medium">
                  📋 Orders:
                </span>
                <strong className="text-slate-50 text-lg font-bold">
                  {Math.round(region.num_orders)}
                </strong>
              </div>
              <div className="flex items-center justify-between group-hover:translate-x-1 transition-smooth duration-300">
                <span className="text-slate-200 text-sm font-medium">
                  💵 Revenue:
                </span>
                <strong className="text-green-300 text-lg font-bold">
                  ₹{region.total_revenue?.toFixed(2) || "0.00"}
                </strong>
              </div>
              <div className="flex items-center justify-between pt-3 border-t border-purple-400/40 group-hover:translate-x-1 transition-smooth duration-300">
                <span className="text-slate-200 text-sm font-medium">
                  📊 Avg/Customer:
                </span>
                <strong className="text-blue-200 text-lg font-bold">
                  ₹{region.avg_revenue_per_customer?.toFixed(2) || "0.00"}
                </strong>
              </div>
            </div>
          </motion.div>
        ))}
      </motion.div>
    </motion.div>
  );
}
