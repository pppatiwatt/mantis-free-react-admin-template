// assets
import { AreaChartOutlined } from '@ant-design/icons';

// icons
const icons = {
  AreaChartOutlined
};

// ==============================|| MENU ITEMS - ANALYZE ||============================== //

const analyze = {
  id: 'group-analyze',
  title: 'Analysis',
  type: 'group',
  children: [
    {
      id: 'analyze',
      title: 'Analyze Data',
      type: 'item',
      url: '/dashboard/analyze',
      icon: icons.AreaChartOutlined,
      breadcrumbs: false
    }
  ]
};

export default analyze;
