export default function ConfidenceGauge({ value }: { value: number }) {
  const percent = Math.round(value * 100);
  return (
    <div className="flex items-center gap-4">
      <div className="relative h-16 w-16 rounded-full bg-gradient-to-br from-mint/20 to-ocean/20 border-2 border-mint/30">
        <div
          className="gradient-ring absolute inset-0 rounded-full"
          style={{
            maskImage: "radial-gradient(circle, transparent 55%, black 56%)",
            WebkitMaskImage: "radial-gradient(circle, transparent 55%, black 56%)",
            transform: `rotate(${percent * 1.8}deg)`
          }}
        />
        <div className="absolute inset-2 rounded-full bg-white" />
        <div className="absolute inset-0 flex items-center justify-center text-sm font-bold text-ocean">
          {percent}%
        </div>
      </div>
      <div>
        <p className="text-sm text-mint/70 font-semibold">🎯 Confidence</p>
        <p className="text-lg font-bold text-ocean">{percent}%</p>
      </div>
    </div>
  );
}
