import { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import RevenueChart from "@/components/RevenueChart";
import TopCustomersTable from "./components/TopCustomersTable";
import CategoryChart from "./components/CategoryChart";
import RegionalCards from "./components/RegionalCards";

const API_BASE = import.meta.env.VITE_SERVER_URL;

interface DashboardData {
  [key: string]: unknown;
}

function App() {
  const [revenueData, setRevenueData] = useState<DashboardData | null>(null);
  const [topCustomers, setTopCustomers] = useState<DashboardData | null>(null);
  const [categoryData, setCategoryData] = useState<DashboardData | null>(null);
  const [regionData, setRegionData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAllData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [revenue, customers, categories, regions] = await Promise.all([
        axios.get(`${API_BASE}/api/revenue`),
        axios.get(`${API_BASE}/api/top-customers`),
        axios.get(`${API_BASE}/api/categories`),
        axios.get(`${API_BASE}/api/regions`),
      ]);
      setRevenueData(revenue.data);
      setTopCustomers(customers.data);
      setCategoryData(categories.data);
      setRegionData(regions.data);
    } catch (err) {
      setError(
        "Failed to load data. Make sure the backend is running on " + API_BASE
      );
      console.error("API Error:", err);
    }
    setLoading(false);
  };
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchAllData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-900 flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-40 left-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
          <div className="absolute top-1/2 right-20 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        </div>
        <div className="text-center relative z-10">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-400 mx-auto mb-4"></div>
          <p className="text-xl font-semibold text-purple-200">
            Loading dashboard...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-900 flex items-center justify-center">
        <div className="bg-red-900/30 backdrop-blur-md border border-red-500/30 rounded-xl p-6 max-w-md mx-4 animate-fade-in">
          <p className="text-red-300 font-semibold">⚠️ Connection Error</p>
          <p className="text-red-200 mt-2 text-sm">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-900 text-white relative overflow-hidden">
      {/* Animated background orbs */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute top-1/2 right-1/4 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute bottom-20 left-1/2 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
      </div>

      <header className="bg-gradient-to-b from-slate-900/80 via-slate-900/40 to-transparent backdrop-blur-md border-b border-purple-500/10 relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="animate-slide-in-down">
            <h1 className="text-5xl md:text-6xl font-black gradient-text mb-2">
              📊 Analytics Dashboard
            </h1>
            <p className="text-purple-200 text-lg font-light tracking-wide">
              Real-time business insights and performance metrics
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 relative z-10">
        <div className="grid grid-cols-1 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <RevenueChart data={revenueData as any} />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <TopCustomersTable data={topCustomers as any} />
          </motion.div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              <CategoryChart data={categoryData as any} />
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.5, delay: 0.4 }}
            >
              <RegionalCards data={regionData as any} />
            </motion.div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
