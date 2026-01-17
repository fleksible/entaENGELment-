'use client';

import { useState, useMemo } from 'react';
import { Void, VoidFilters } from '@/types';
import { VoidCard } from './VoidCard';
import { VoidFilter } from './VoidFilter';
import { getVoids, getVoidStats } from '@/lib/voidmap-parser';

export function VoidList() {
  const [filters, setFilters] = useState<VoidFilters>({
    status: 'ALL',
    priority: 'ALL',
    domain: 'ALL',
  });
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const voids = getVoids();
  const stats = getVoidStats();

  // Filter voids
  const filteredVoids = useMemo(() => {
    return voids.filter((v) => {
      if (filters.status !== 'ALL' && v.status !== filters.status) {
        return false;
      }
      if (filters.priority !== 'ALL') {
        // Handle 'med' as alias for 'medium'
        const normalizedPriority = v.priority === 'med' ? 'medium' : v.priority;
        const normalizedFilter = filters.priority === 'med' ? 'medium' : filters.priority;
        if (normalizedPriority !== normalizedFilter) {
          return false;
        }
      }
      return true;
    });
  }, [voids, filters]);

  // Sort: Open first, then by priority
  const sortedVoids = useMemo(() => {
    const priorityOrder = { critical: 0, high: 1, medium: 2, med: 2, low: 3 };
    const statusOrder = { OPEN: 0, IN_PROGRESS: 1, CLOSED: 2 };

    return [...filteredVoids].sort((a, b) => {
      // First by status
      const statusDiff = statusOrder[a.status] - statusOrder[b.status];
      if (statusDiff !== 0) return statusDiff;

      // Then by priority
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    });
  }, [filteredVoids]);

  return (
    <div className="space-y-4 md:space-y-6">
      {/* Filters */}
      <VoidFilter
        filters={filters}
        onFilterChange={setFilters}
        stats={stats}
      />

      {/* Results count */}
      <div className="text-sm text-zinc-500">
        {filteredVoids.length} von {voids.length} VOIDs
      </div>

      {/* Void List */}
      <div className="space-y-3">
        {sortedVoids.map((void_item) => (
          <VoidCard
            key={void_item.id}
            void_item={void_item}
            expanded={expandedId === void_item.id}
            onToggle={() => setExpandedId(
              expandedId === void_item.id ? null : void_item.id
            )}
          />
        ))}
      </div>

      {/* Empty state */}
      {sortedVoids.length === 0 && (
        <div className="text-center py-12 text-zinc-500">
          <span className="text-4xl block mb-3">☐</span>
          <p>Keine VOIDs mit diesen Filtern gefunden.</p>
        </div>
      )}
    </div>
  );
}
