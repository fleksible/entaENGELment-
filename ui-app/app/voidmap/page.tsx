import { VoidList } from '@/components/voidmap/VoidList';
import { getVoidStats } from '@/lib/voidmap-parser';

export default function VoidMapPage() {
  const stats = getVoidStats();

  return (
    <div className="space-y-6 md:space-y-8">
      {/* Header */}
      <header className="pt-2 md:pt-4">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-3xl">☐</span>
          <h1 className="text-2xl md:text-3xl font-bold text-zinc-100">
            VOIDMAP Explorer
          </h1>
        </div>
        <p className="text-sm md:text-base text-zinc-500">
          Central registry for tracking open voids (gaps) in the entaENGELment framework.
        </p>
      </header>

      {/* Quick Stats */}
      <div className="grid grid-cols-4 gap-2 md:gap-4">
        <div className="bg-zinc-900/30 rounded-lg p-3 md:p-4 text-center">
          <div className="text-xl md:text-2xl font-bold text-zinc-100">
            {stats.total}
          </div>
          <div className="text-[10px] md:text-xs text-zinc-500">Total</div>
        </div>
        <div className="bg-amber-500/10 rounded-lg p-3 md:p-4 text-center border border-amber-500/20">
          <div className="text-xl md:text-2xl font-bold text-amber-400">
            {stats.open}
          </div>
          <div className="text-[10px] md:text-xs text-amber-500/70">Open</div>
        </div>
        <div className="bg-blue-500/10 rounded-lg p-3 md:p-4 text-center border border-blue-500/20">
          <div className="text-xl md:text-2xl font-bold text-blue-400">
            {stats.inProgress}
          </div>
          <div className="text-[10px] md:text-xs text-blue-500/70">Progress</div>
        </div>
        <div className="bg-green-500/10 rounded-lg p-3 md:p-4 text-center border border-green-500/20">
          <div className="text-xl md:text-2xl font-bold text-green-400">
            {stats.closed}
          </div>
          <div className="text-[10px] md:text-xs text-green-500/70">Closed</div>
        </div>
      </div>

      {/* VOID List */}
      <VoidList />
    </div>
  );
}
