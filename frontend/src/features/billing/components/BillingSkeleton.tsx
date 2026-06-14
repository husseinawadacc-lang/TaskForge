export default function BillingSkeleton() {

  return (

    <div className="space-y-4 animate-pulse">

      <div className="h-40 bg-gray-200 rounded-xl" />

      <div className="grid grid-cols-2 gap-4">

        <div className="h-12 bg-gray-200 rounded" />

        <div className="h-12 bg-gray-200 rounded" />

        <div className="h-12 bg-gray-200 rounded" />

        <div className="h-12 bg-gray-200 rounded" />

      </div>

    </div>

  )
}