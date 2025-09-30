import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

interface SentimentChartProps {
  distribution: {
    positive: number;
    negative: number;
    neutral: number;
  };
}

const SentimentChart: React.FC<SentimentChartProps> = ({ distribution }) => {
  const data = [
    { name: 'Positive', value: distribution.positive, emoji: '😊' },
    { name: 'Negative', value: distribution.negative, emoji: '😞' },
    { name: 'Neutral', value: distribution.neutral, emoji: '😐' },
  ];

  const COLORS = ['#10b981', '#ef4444', '#6b7280'];

  const renderLabel = (entry: any) => {
    return `${entry.emoji} ${entry.value.toFixed(1)}%`;
  };

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={renderLabel}
          outerRadius={100}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(value: any) => `${value.toFixed(1)}%`} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default SentimentChart;
