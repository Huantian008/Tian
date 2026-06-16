export default function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center h-full">
      <div className="relative">
        <div
          className="w-12 h-12 rounded-full border-2 border-transparent spinner"
          style={{
            borderTopColor: '#0f8f68',
            borderRightColor: 'rgba(15, 143, 104, 0.24)',
          }}
        />
        <div
          className="absolute inset-0 w-12 h-12 rounded-full"
          style={{
            background: 'radial-gradient(circle, rgba(15, 143, 104, 0.12) 0%, transparent 70%)',
          }}
        />
      </div>
    </div>
  );
}
