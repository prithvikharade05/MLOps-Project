"use client"

import { motion } from "framer-motion"
import { Sparkles, Zap, Brain, Shield, Clock, TrendingUp } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-indigo-900/30 to-cyan-900/30">
      {/* Animated 3D Particles Background */}
      <div className="fixed inset-0 opacity-20">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-cyan-500/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute top-1/2 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="absolute bottom-1/4 left-1/2 w-80 h-80 bg-pink-500/20 rounded-full blur-3xl animate-pulse delay-2000" />
      </div>

      <div className="relative z-10 container mx-auto px-6 py-12">
        <motion.div 
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-24"
        >
          <div className="inline-flex items-center gap-3 bg-gradient-to-r from-cyan-500 to-blue-500 bg-clip-text text-transparent text-2xl mb-4 animate-pulse">
            <Zap className="w-8 h-8" />
            BTC FORECASTING MLOps PLATFORM
          </div>
          <h1 className="text-6xl md:text-7xl font-black bg-gradient-to-r from-white via-cyan-100 to-blue-100 bg-clip-text text-transparent mb-6">
            Institutional Grade
          </h1>
          <p className="text-xl md:text-2xl text-cyan-100/80 max-w-3xl mx-auto leading-relaxed">
            Real-time Bitcoin forecasting with enterprise MLOps pipeline. 
            Engineered for hedge funds, trading firms, and quantitative analysts.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 mt-12 justify-center">
            <Button size="lg" className="bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 text-lg px-8 py-6 font-semibold shadow-2xl shadow-cyan-500/25 neon-glow">
              Live Dashboard
            </Button>
            <Button size="lg" variant="outline" className="border-white/30 backdrop-blur-sm text-lg px-8 py-6 font-semibold">
              API Docs
            </Button>
          </div>
        </motion.div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="futuristic-card"
          >
            <Card className="glass-panel border-none bg-gradient-to-br from-cyan-500/5 to-blue-500/5 backdrop-blur-xl">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl flex items-center justify-center mb-4 neon-glow">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-2xl font-black text-white">Real-Time Data</CardTitle>
                <CardDescription className="text-cyan-100">
                  Live Binance BTC/USDT feed with sub-minute latency. Never miss a market move.
                </CardDescription>
              </CardHeader>
            </Card>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="futuristic-card"
          >
            <Card className="glass-panel border-none bg-gradient-to-br from-purple-500/5 to-pink-500/5 backdrop-blur-xl">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mb-4 neon-glow">
                  <Brain className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-2xl font-black text-white">MLflow MLOps</CardTitle>
                <CardDescription className="text-purple-100">
                  Full experiment tracking, model registry, and automated retraining pipelines.
                </CardDescription>
              </CardHeader>
            </Card>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="futuristic-card"
          >
            <Card className="glass-panel border-none bg-gradient-to-br from-emerald-500/5 to-teal-500/5 backdrop-blur-xl">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center mb-4 neon-glow">
                  <Shield className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-2xl font-black text-white">Drift Detection</CardTitle>
                <CardDescription className="text-emerald-100">
                  PSI & KS-test monitoring with automatic alerts. Models stay sharp in all markets.
                </CardDescription>
              </CardHeader>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

