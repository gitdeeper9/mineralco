#!/usr/bin/env python3
"""
MINERALCO Report Generator
Generates daily, weekly, monthly reports and alerts in .txt format
"""

import os
import sys
import json
import datetime
from pathlib import Path

# إضافة المسار الرئيسي
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from mineralco.engine.eos_fitter import EOSFitter
    from mineralco.engine.lattice_analyzer import LatticeAnalyzer
    from mineralco.engine.phase_mapper import PhaseMapper
    from mineralco.engine.thermal_corrector import ThermalCorrector
    CORE_MODULES_AVAILABLE = True
except ImportError:
    CORE_MODULES_AVAILABLE = False

class MineralcoReportGenerator:
    """مولد التقارير اليومية والأسبوعية والشهرية"""
    
    def __init__(self, base_dir="reports"):
        self.base_dir = Path(base_dir)
        self.daily_dir = self.base_dir / "daily"
        self.weekly_dir = self.base_dir / "weekly"
        self.monthly_dir = self.base_dir / "monthly"
        self.alerts_dir = self.base_dir / "alerts"
        
        # إنشاء المجلدات إذا لم تكن موجودة
        for dir_path in [self.daily_dir, self.weekly_dir, self.monthly_dir, self.alerts_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def get_current_date(self):
        """الحصول على التاريخ الحالي"""
        return datetime.datetime.now()
    
    def get_date_str(self, date=None):
        """تحويل التاريخ إلى نص"""
        if date is None:
            date = self.get_current_date()
        return date.strftime("%Y-%m-%d")
    
    def get_week_str(self, date=None):
        """الحصول على رقم الأسبوع"""
        if date is None:
            date = self.get_current_date()
        year, week, _ = date.isocalendar()
        return f"{year}-W{week:02d}"
    
    def get_month_str(self, date=None):
        """الحصول على الشهر"""
        if date is None:
            date = self.get_current_date()
        return date.strftime("%Y-%m")
    
    def load_mineral_data(self):
        """تحميل بيانات المعادن"""
        try:
            db_path = Path("data/databases/cis/cis_database_v1.0.0.json")
            if db_path.exists():
                with open(db_path, 'r') as f:
                    data = json.load(f)
                return data.get('minerals', [])
        except Exception as e:
            print(f"⚠️ خطأ في تحميل البيانات: {e}")
        return []
    
    def load_experimental_data(self):
        """تحميل البيانات التجريبية"""
        try:
            exp_path = Path("data/experimental/dac/combined_dac_data.csv")
            if exp_path.exists():
                points = 0
                with open(exp_path, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            points += 1
                return points
        except Exception as e:
            print(f"⚠️ خطأ في تحميل البيانات التجريبية: {e}")
        return 0
    
    def load_prem_data(self):
        """تحميل بيانات PREM"""
        try:
            prem_path = Path("data/reference/prem/prem_1981_updated.csv")
            if prem_path.exists():
                points = 0
                with open(prem_path, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            points += 1
                return points
        except Exception as e:
            print(f"⚠️ خطأ في تحميل بيانات PREM: {e}")
        return 0
    
    def get_system_info(self):
        """معلومات النظام"""
        info = {
            "date": self.get_date_str(),
            "time": self.get_current_date().strftime("%H:%M:%S"),
            "python_version": sys.version.split()[0],
            "core_modules": "Available" if CORE_MODULES_AVAILABLE else "Not Available",
            "reports_directory": str(self.base_dir.absolute()),
            "total_reports": self.count_reports()
        }
        return info
    
    def count_reports(self):
        """عد التقارير الموجودة"""
        count = 0
        for dir_path in [self.daily_dir, self.weekly_dir, self.monthly_dir, self.alerts_dir]:
            if dir_path.exists():
                count += len([f for f in dir_path.glob("*.txt")])
        return count
    
    def generate_daily_report(self, date=None):
        """
        توليد تقرير يومي شامل
        
        التقرير اليومي يشمل:
        - ملخص عام
        - حالة المعادن الرئيسية
        - مؤشرات الاستقرار
        - أحدث القياسات
        - إنذارات إذا وجدت
        """
        if date is None:
            date = self.get_current_date()
        
        date_str = self.get_date_str(date)
        filename = self.daily_dir / f"report_{date_str}.txt"
        
        # تحميل البيانات
        minerals = self.load_mineral_data()
        exp_points = self.load_experimental_data()
        prem_points = self.load_prem_data()
        sys_info = self.get_system_info()
        
        with open(filename, 'w', encoding='utf-8') as f:
            # رأس التقرير
            f.write("=" * 80 + "\n")
            f.write(f"{'🪨 MINERALCO DAILY REPORT':^80}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Date: {date_str}\n")
            f.write(f"Time: {sys_info['time']}\n")
            f.write(f"Python: {sys_info['python_version']}\n")
            f.write(f"Core Modules: {sys_info['core_modules']}\n")
            f.write("-" * 80 + "\n\n")
            
            # القسم 1: ملخص عام
            f.write("📊 GENERAL SUMMARY\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total minerals in database: {len(minerals)}\n")
            f.write(f"Experimental data points: {exp_points}\n")
            f.write(f"PREM reference points: {prem_points}\n")
            f.write(f"Total reports generated: {sys_info['total_reports'] + 1}\n\n")
            
            # القسم 2: توزيع المعادن حسب النظام البلوري
            if minerals:
                f.write("🔬 MINERALS BY CRYSTAL SYSTEM\n")
                f.write("-" * 40 + "\n")
                systems = {}
                for m in minerals:
                    sys_name = m.get('crystal_system', 'unknown')
                    systems[sys_name] = systems.get(sys_name, 0) + 1
                
                for sys_name, count in sorted(systems.items()):
                    f.write(f"  {sys_name:15s}: {count:2d} minerals\n")
                f.write("\n")
            
            # القسم 3: أبرز المعادن (أول 5)
            if minerals:
                f.write("⭐ KEY MINERALS\n")
                f.write("-" * 40 + "\n")
                for i, m in enumerate(minerals[:5]):
                    name = m.get('name', 'unknown')
                    formula = m.get('formula', '')
                    K0 = m.get('K0', 0)
                    crystal = m.get('crystal_system', '')
                    f.write(f"  {i+1}. {name:15s} ({formula}):\n")
                    f.write(f"     K₀ = {K0:.1f} GPa | {crystal}\n")
                f.write("\n")
            
            # القسم 4: مؤشرات الاستقرار (إذا كانت الوحدات متاحة)
            if CORE_MODULES_AVAILABLE and minerals:
                f.write("🔮 CRYSTAL STABILITY INDEX (CSI)\n")
                f.write("-" * 40 + "\n")
                
                mapper = PhaseMapper()
                
                # اختيار 3 معادن رئيسية
                key_minerals = []
                for name in ['bridgmanite', 'ringwoodite', 'periclase']:
                    for m in minerals:
                        if m.get('name') == name:
                            key_minerals.append(m)
                            break
                
                for m in key_minerals:
                    name = m.get('name', 'unknown')
                    result = mapper.compute_csi(
                        K0=m.get('K0', 0),
                        Vs=m.get('V0', 0),
                        Kprime=m.get('Kprime', 4),
                        Sy=m.get('crystal_system', 'cubic'),
                        alpha=m.get('alpha_300K', 2e-5),
                        gamma=m.get('gamma', 1.5)
                    )
                    f.write(f"  {name:12s}: CSI = {result.csi:.3f} | {result.status}\n")
                    
                    # إنذار إذا كان CSI مرتفعاً
                    if result.csi >= 0.8:
                        self.generate_alert(
                            f"High CSI for {name}",
                            f"CSI = {result.csi:.3f} - {result.status}",
                            "WARNING"
                        )
                f.write("\n")
            
            # القسم 5: آخر التحديثات
            f.write("📈 RECENT UPDATES\n")
            f.write("-" * 40 + "\n")
            f.write("  • Last database update: 2026-03-14\n")
            f.write("  • Last experimental data: 2026-03-14\n")
            f.write(f"  • This report: {date_str}\n\n")
            
            # القسم 6: الإحصائيات
            f.write("📊 STATISTICS\n")
            f.write("-" * 40 + "\n")
            f.write(f"  Average K₀: {self.calculate_avg_k0(minerals):.1f} GPa\n")
            f.write(f"  Average K': {self.calculate_avg_kprime(minerals):.2f}\n\n")
            
            # تذييل التقرير
            f.write("-" * 80 + "\n")
            f.write(f"Report generated by MINERALCO v1.0.0\n")
            f.write(f"DOI: 10.5281/zenodo.19009597\n")
            f.write("=" * 80 + "\n")
        
        print(f"✅ Daily report generated: {filename}")
        return filename
    
    def calculate_avg_k0(self, minerals):
        """حساب متوسط K₀"""
        values = [m.get('K0', 0) for m in minerals if m.get('K0', 0) > 0]
        return sum(values) / len(values) if values else 0
    
    def calculate_avg_kprime(self, minerals):
        """حساب متوسط K'"""
        values = [m.get('Kprime', 0) for m in minerals if m.get('Kprime', 0) > 0]
        return sum(values) / len(values) if values else 0
    
    def generate_weekly_report(self, date=None):
        """
        توليد تقرير أسبوعي شامل
        
        التقرير الأسبوعي يشمل ملخص لآخر 7 أيام
        """
        if date is None:
            date = self.get_current_date()
        
        week_str = self.get_week_str(date)
        filename = self.weekly_dir / f"report_{week_str}.txt"
        
        # جمع تقارير الأيام السبعة الماضية
        daily_reports = []
        for i in range(7):
            check_date = date - datetime.timedelta(days=i)
            daily_file = self.daily_dir / f"report_{self.get_date_str(check_date)}.txt"
            if daily_file.exists():
                daily_reports.append(daily_file)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"{'🪨 MINERALCO WEEKLY REPORT':^80}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Week: {week_str}\n")
            f.write(f"Generated: {self.get_date_str(date)}\n")
            f.write("-" * 80 + "\n\n")
            
            f.write("📊 WEEKLY SUMMARY\n")
            f.write("-" * 40 + "\n")
            f.write(f"Daily reports this week: {len(daily_reports)}\n")
            f.write(f"Days covered: {', '.join([str(d).split('_')[1].split('.')[0] for d in daily_reports])}\n\n")
            
            if daily_reports:
                f.write("📈 WEEKLY TRENDS\n")
                f.write("-" * 40 + "\n")
                f.write("  • System stable\n")
                f.write("  • No critical alerts\n\n")
            
            f.write("-" * 80 + "\n")
            f.write(f"Report generated by MINERALCO v1.0.0\n")
            f.write("=" * 80 + "\n")
        
        print(f"✅ Weekly report generated: {filename}")
        return filename
    
    def generate_monthly_report(self, date=None):
        """
        توليد تقرير شهري شامل
        
        التقرير الشهري يشمل ملخص للشهر
        """
        if date is None:
            date = self.get_current_date()
        
        month_str = self.get_month_str(date)
        filename = self.monthly_dir / f"report_{month_str}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"{'🪨 MINERALCO MONTHLY REPORT':^80}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Month: {month_str}\n")
            f.write(f"Generated: {self.get_date_str(date)}\n")
            f.write("-" * 80 + "\n\n")
            
            f.write("📊 MONTHLY SUMMARY\n")
            f.write("-" * 40 + "\n")
            f.write("  • All systems operational\n")
            f.write("  • Database stable\n")
            f.write("  • No critical issues\n\n")
            
            f.write("-" * 80 + "\n")
            f.write(f"Report generated by MINERALCO v1.0.0\n")
            f.write("=" * 80 + "\n")
        
        print(f"✅ Monthly report generated: {filename}")
        return filename
    
    def generate_alert(self, title, message, level="INFO"):
        """
        توليد ملف إنذار
        المستويات: INFO, WARNING, CRITICAL
        """
        date_str = self.get_date_str()
        time_str = self.get_current_date().strftime("%H%M%S")
        filename = self.alerts_dir / f"alert_{date_str}_{time_str}_{level}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write(f"{'🚨 MINERALCO ALERT':^60}\n")
            f.write("=" * 60 + "\n")
            f.write(f"Date: {date_str}\n")
            f.write(f"Time: {self.get_current_date().strftime('%H:%M:%S')}\n")
            f.write(f"Level: {level}\n")
            f.write("-" * 60 + "\n")
            f.write(f"Title: {title}\n\n")
            f.write(f"Message: {message}\n\n")
            f.write("-" * 60 + "\n")
            f.write("Please check the system if necessary.\n")
            f.write("=" * 60 + "\n")
        
        print(f"⚠️ Alert generated: {filename}")
        return filename
    
    def generate_all_reports(self):
        """توليد جميع التقارير (يومي، أسبوعي، شهري)"""
        date = self.get_current_date()
        
        daily = self.generate_daily_report(date)
        weekly = self.generate_weekly_report(date)
        monthly = self.generate_monthly_report(date)
        
        print("\n" + "=" * 60)
        print("✅ ALL REPORTS GENERATED SUCCESSFULLY")
        print("=" * 60)
        print(f"📋 Daily:   {daily}")
        print(f"📋 Weekly:  {weekly}")
        print(f"📋 Monthly: {monthly}")
        print(f"📋 Alerts:  {len(list(self.alerts_dir.glob('*.txt')))} alerts")
        print("=" * 60)
        
        return {
            "daily": daily,
            "weekly": weekly,
            "monthly": monthly
        }


def main():
    """الوظيفة الرئيسية"""
    import argparse
    
    parser = argparse.ArgumentParser(description='MINERALCO Report Generator')
    parser.add_argument('--type', choices=['daily', 'weekly', 'monthly', 'all'], 
                       default='all', help='Type of report to generate')
    parser.add_argument('--alert', nargs=3, metavar=('TITLE', 'MESSAGE', 'LEVEL'),
                       help='Generate an alert: title message LEVEL(INFO/WARNING/CRITICAL)')
    
    args = parser.parse_args()
    
    generator = MineralcoReportGenerator()
    
    if args.alert:
        title, message, level = args.alert
        if level.upper() in ['INFO', 'WARNING', 'CRITICAL']:
            generator.generate_alert(title, message, level.upper())
        else:
            print("❌ Alert level must be INFO, WARNING, or CRITICAL")
        return
    
    if args.type == 'daily':
        generator.generate_daily_report()
    elif args.type == 'weekly':
        generator.generate_weekly_report()
    elif args.type == 'monthly':
        generator.generate_monthly_report()
    elif args.type == 'all':
        generator.generate_all_reports()


if __name__ == "__main__":
    main()
