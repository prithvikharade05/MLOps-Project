"use client"

import { motion } from "framer-motion"
import { AlertCircle, ShieldCheck, Activity, TrendingDown } from "lucide-react"

export default function MonitoringPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900/30 to-slate-900">
      <div className="container mx-auto px-6 py-12">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center gap-3 bg-gradient-to-r from-orange-500 to-red-500 bg-clip-text text-transparent text-3xl mb-6">
            <ShieldCheck className="w-12 h-12" />
            Drift Monitoring Dashboard
          </div>
          <h1 className="text-5xl md:text-6xl font-black bg-gradient-to-r from-white to-orange-100 bg-clip-text text-transparent mb-4">
            Model Health Center
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Real-time drift detection and model performance tracking. 
            PSI, KS-test, and automated alerts keep your models production ready.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
          {/* Drift Heatmap */}
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="futuristic-card col-span-1 lg:col-span-2"
          >
            <Card className="glass-panel border-none h-[500px]">
              <CardHeader>
                <CardTitle className="text-2xl font-black text-white flex items-center gap-2">
                  <Activity className="w-8 h-8" />
                  Drift Heatmap (Last 24h)
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                <div className="grid grid-cols-2 gap-4 h-96">
                  <div className="bg-gradient-to-br from-orange-500/20 to-red-500/20 rounded-2xl p-6 backdrop-blur-xl border border-orange-500/30">
                    <div className="text-3xl font-black text-orange-400 mb-2">RSI</div>
                    <div className="text-sm text-orange-200 mb-4">PSI: 0.25</div>
                    <div className="w-full bg-gradient-to-r from-orange-500/20 to-transparent rounded-full h-3">
                      <div className="bg-gradient-to-r from-orange-500 to-red-500 h-3 rounded-full w-75%" />
                    </div>
                  </div>
                  {/* More feature cards */}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Active Alerts */}
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="futuristic-card"
          >
            <Card className="glass-panel border-none h-[300px]">
              <CardHeader>
                <CardTitle className="text-xl font-black text-white flex items-center gap-2 text-red-400">
                  <AlertCircle className="w-6 h-6" />
                  Active Alerts (3)
                </CardTitle>
              </CardHeader>
              <CardContent className="p-4 space-y-3">
                <div className="flex items-center gap-3 p-3 bg-gradient-to-r from-red-500/10 to-orange-500/10 rounded-xl border border-red-500/20">
                  <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
                  <div>
                    <div className="font-semibold text-red-300 text-sm">RSI Drift HIGH</div>
                    <div className="text-xs text-red-400">2h ago</div>
                  </div>
                </div>
                {/* More alerts */}
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

