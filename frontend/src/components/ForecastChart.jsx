import {
  AreaChart,
  CartesianGrid,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

export default function ForecastChart({ data, y1, y2, xAxis }) {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          {payload.map((i, index) => {
            if (index === 0) {
              console.log(i)
              return (
                <div className="bg-white border rounded p-3 flex flex-col" key={i.value}>
                  <div className="flex flex-row justify-between items-center mb-2">
                    <p className="font-medium text-black/[.7]">Sales</p>
                    <p className="text-black/[.7] text-sm">{label}</p>
                  </div>
                  {i.payload.sales ?
                    <p className="text-base text-[#8884d8]">Actual: ₱{i.payload.sales.toLocaleString()}</p>
                    : ""}
                  <p className="text-base text-[#51b877]">Predicted: ₱{i.payload.predicted.toLocaleString()}</p>
                </div>
              )
            }
            return
          })}

        </div>
      );
    }

    return null;
  }

  return (
    <ResponsiveContainer width="100%" height="100%">
      <AreaChart data={data}
        margin={{ top: 5, right: 20, bottom: 50, left: 0 }}>
        <defs>
          <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
            <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8} />
            <stop offset="95%" stopColor="#82ca9d" stopOpacity={0} />
          </linearGradient>
        </defs>
        <XAxis dataKey={xAxis} />
        <YAxis />
        <CartesianGrid strokeDasharray="3 3" />
        <Tooltip wrapperStyle={{ outline: "none" }} cursor={{ fill: 'transparent' }} content={<CustomTooltip />} />
        <Area type="monotone" dataKey={y1} stroke="#8884d8" fillOpacity={1} fill="url(#colorUv)" />
        <Area type="monotone" dataKey={y2} stroke="#82ca9d" fillOpacity={1} fill="url(#colorPv)" />
      </AreaChart>
    </ResponsiveContainer>
  );
}