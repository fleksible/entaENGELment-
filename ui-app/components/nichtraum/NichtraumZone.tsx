'use client';

interface NichtraumZoneProps {
  id: string;
  name: string;
  description: string;
  icon: string;
  itemCount: number;
}

export function NichtraumZone({ id, name, description, icon, itemCount }: NichtraumZoneProps) {
  return (
    <div className="
      relative
      p-6 md:p-8
      bg-zinc-950
      rounded-2xl
      border-2 border-dashed border-zinc-800
      overflow-hidden
    ">
      {/* Background pattern - "emptiness" visualization */}
      <div className="
        absolute inset-0
        opacity-5
        bg-[radial-gradient(circle_at_center,_transparent_0%,_transparent_50%,_#27272a_50%,_#27272a_100%)]
        bg-[length:20px_20px]
      " />

      {/* Content */}
      <div className="relative z-10">
        {/* Icon */}
        <span className="text-4xl mb-4 block opacity-50">{icon}</span>

        {/* Name */}
        <h3 className="text-lg font-medium text-zinc-400 mb-1">
          {name}
        </h3>

        {/* Description */}
        <p className="text-sm text-zinc-600">
          {description}
        </p>

        {/* Item count */}
        <div className="mt-4 flex items-center gap-2">
          <span className="
            px-3 py-1.5
            bg-zinc-900 rounded-full
            text-xs text-zinc-500
            border border-zinc-800
          ">
            {itemCount === 0 ? 'Leer' : `${itemCount} Items`}
          </span>
        </div>

        {/* Intentionally empty message */}
        {itemCount === 0 && (
          <div className="mt-4 p-3 bg-zinc-900/50 rounded-lg border border-zinc-800/50">
            <p className="text-xs text-zinc-600 italic">
              &ldquo;Dieser Raum ist absichtlich leer.
              Hier liegt, was noch nicht entschieden ist.&rdquo;
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
