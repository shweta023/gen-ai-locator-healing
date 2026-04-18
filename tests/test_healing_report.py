"""Test to generate and display healing reports"""

import pytest
import json
import os
from datetime import datetime
from tabulate import tabulate


class TestHealingReport:
    """Tests focused on healing functionality and reporting"""

    @pytest.mark.healing
    def test_generate_healing_report(self, smart_finder):
        """Generate and save healing report"""
        print("\n" + "=" * 70)
        print("🧪 TEST: Generate Healing Report")
        print("=" * 70)

        report = smart_finder.get_healing_report()

        if report:
            # Save report to file
            report_dir = "reports"
            os.makedirs(report_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = os.path.join(report_dir, f"healing_report_{timestamp}.json")

            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)

            print(f"\n📊 Healing report saved to: {report_file}")
            print(f"📈 Total healings: {len(report)}")

            # Print summary
            high_confidence = sum(1 for r in report if r['confidence'] == 'high')
            medium_confidence = sum(1 for r in report if r['confidence'] == 'medium')
            low_confidence = sum(1 for r in report if r['confidence'] == 'low')

            print(f"\n📊 Healing Statistics:")
            print(f"   High Confidence: {high_confidence}")
            print(f"   Medium Confidence: {medium_confidence}")
            print(f"   Low Confidence: {low_confidence}")
            print(f"   Success Rate: {(high_confidence / len(report) * 100):.1f}%")

            # Create table for display
            table_data = []
            for entry in report:
                table_data.append([
                    entry['locator_name'][:30],
                    entry['old_by'],
                    entry['old_value'][:30] + '...' if len(entry['old_value']) > 30 else entry['old_value'],
                    entry['new_by'],
                    entry['new_value'][:30] + '...' if len(entry['new_value']) > 30 else entry['new_value'],
                    entry['confidence']
                ])

            headers = ['Locator', 'Old By', 'Old Value', 'New By', 'New Value', 'Confidence']
            print("\n" + tabulate(table_data, headers=headers, tablefmt='grid'))

        else:
            print("✅ No healings occurred during this test session")
            print("   All locators are working perfectly! 🎉")

        print("\n✅ TEST PASSED: Report generation complete!")

    @pytest.mark.healing
    def test_display_healing_report(self, smart_finder):
        """Display detailed healing report"""
        print("\n" + "=" * 70)
        print("🧪 TEST: Display Detailed Healing Report")
        print("=" * 70)

        smart_finder.print_healing_report()

        report = smart_finder.get_healing_report()

        if report:
            print("\n📝 Detailed Healing Information:")

            for i, entry in enumerate(report, 1):
                print(f"\n{'─' * 70}")
                print(f"Healing #{i}")
                print(f"{'─' * 70}")
                print(f"  🏷️  Locator Name: {entry['locator_name']}")
                print(f"  📄 Page: {entry['page']}")
                print(f"  🕐 Timestamp: {entry['timestamp']}")
                print(f"\n  ❌ OLD LOCATOR:")
                print(f"     Strategy: {entry['old_by']}")
                print(f"     Value: {entry['old_value']}")
                print(f"\n  ✅ NEW LOCATOR:")
                print(f"     Strategy: {entry['new_by']}")
                print(f"     Value: {entry['new_value']}")
                print(f"\n  📊 Confidence: {entry['confidence'].upper()}")
                print(f"  💡 Reasoning: {entry['reasoning']}")

        print("\n✅ TEST PASSED: Detailed report displayed!")

    @pytest.mark.healing
    def test_locator_registry_status(self, locator_registry):
        """Display current locator registry status"""
        print("\n" + "=" * 70)
        print("🧪 TEST: Locator Registry Status")
        print("=" * 70)

        print("\n" + "=" * 70)
        print("📋 LOCATOR REGISTRY STATUS")
        print("=" * 70)

        all_locators = locator_registry.get_all_locators()

        # Group by page
        pages = {}
        for name, locator in all_locators.items():
            page = locator.page
            if page not in pages:
                pages[page] = []
            pages[page].append((name, locator))

        # Display by page
        for page, locators in sorted(pages.items()):
            print(f"\n📄 Page: {page.upper()}")
            print("─" * 70)

            for name, locator in locators:
                print(f"\n  🔖 {name}")
                print(f"     Strategy: {locator.by}")
                print(f"     Value: {locator.value}")
                print(f"     Description: {locator.description}")
                print(f"     Failures: {locator.failure_count}")
                print(f"     Last Updated: {locator.last_updated}")

        print("\n" + "=" * 70)
        print(f"📊 Total Locators: {len(all_locators)}")
        print(f"📄 Total Pages: {len(pages)}")
        print("=" * 70)

        print("\n✅ TEST PASSED: Registry status displayed!")

    @pytest.mark.healing
    def test_locator_failure_tracking(self, locator_registry):
        """Test and display locator failure tracking"""
        print("\n" + "=" * 70)
        print("🧪 TEST: Locator Failure Tracking")
        print("=" * 70)

        all_locators = locator_registry.get_all_locators()

        # Find locators with failures
        failed_locators = [
            (name, loc) for name, loc in all_locators.items()
            if loc.failure_count > 0
        ]

        if failed_locators:
            print(f"\n⚠️  Found {len(failed_locators)} locator(s) with failures:")

            table_data = []
            for name, loc in failed_locators:
                table_data.append([
                    name,
                    loc.page,
                    loc.failure_count,
                    loc.by,
                    loc.value[:40] + '...' if len(loc.value) > 40 else loc.value,
                    loc.last_updated[:19]  # Trim to datetime only
                ])

            headers = ['Locator', 'Page', 'Failures', 'Strategy', 'Value', 'Last Updated']
            print("\n" + tabulate(table_data, headers=headers, tablefmt='grid'))

            print("\n💡 Tip: Locators with high failure counts may need manual review")
        else:
            print("\n✅ No locators have recorded failures!")
            print("   All locators are stable and reliable.")

        print("\n✅ TEST PASSED: Failure tracking verified!")

    @pytest.mark.healing
    def test_healing_statistics(self, smart_finder, locator_registry):
        """Generate comprehensive healing statistics"""
        print("\n" + "=" * 70)
        print("🧪 TEST: Healing Statistics Analysis")
        print("=" * 70)

        report = smart_finder.get_healing_report()
        all_locators = locator_registry.get_all_locators()

        # Overall statistics
        total_locators = len(all_locators)
        healed_locators = len(report)
        stable_locators = total_locators - healed_locators

        print("\n📊 OVERALL STATISTICS")
        print("=" * 70)
        print(f"  Total Locators: {total_locators}")
        print(f"  Stable Locators: {stable_locators}")
        print(f"  Healed Locators: {healed_locators}")
        if total_locators > 0:
            print(f"  Stability Rate: {(stable_locators / total_locators * 100):.1f}%")

        if report:
            # Confidence breakdown
            confidence_count = {
                'high': sum(1 for r in report if r['confidence'] == 'high'),
                'medium': sum(1 for r in report if r['confidence'] == 'medium'),
                'low': sum(1 for r in report if r['confidence'] == 'low')
            }

            print("\n📊 HEALING CONFIDENCE BREAKDOWN")
            print("=" * 70)
            for level, count in confidence_count.items():
                percentage = (count / len(report) * 100) if len(report) > 0 else 0
                print(f"  {level.capitalize()}: {count} ({percentage:.1f}%)")

            # Strategy changes
            strategy_changes = {}
            for entry in report:
                change = f"{entry['old_by']} → {entry['new_by']}"
                strategy_changes[change] = strategy_changes.get(change, 0) + 1

            print("\n📊 STRATEGY CHANGES")
            print("=" * 70)
            for change, count in sorted(strategy_changes.items(), key=lambda x: x[1], reverse=True):
                print(f"  {change}: {count}")

            # Page breakdown
            page_healings = {}
            for entry in report:
                page = entry['page']
                page_healings[page] = page_healings.get(page, 0) + 1

            print("\n📊 HEALINGS BY PAGE")
            print("=" * 70)
            for page, count in sorted(page_healings.items(), key=lambda x: x[1], reverse=True):
                print(f"  {page}: {count}")

        print("\n✅ TEST PASSED: Statistics generated successfully!")

    @pytest.mark.healing
    def test_export_healing_summary(self, smart_finder, locator_registry):
        """Export healing summary to multiple formats"""
        print("\n" + "=" * 70)
        print("🧪 TEST: Export Healing Summary")
        print("=" * 70)

        report = smart_finder.get_healing_report()

        # Create reports directory
        report_dir = "reports"
        os.makedirs(report_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Export as JSON (detailed)
        json_file = os.path.join(report_dir, f"healing_detailed_{timestamp}.json")
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✅ Detailed JSON report: {json_file}")

        # Export as summary text
        txt_file = os.path.join(report_dir, f"healing_summary_{timestamp}.txt")
        with open(txt_file, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("GenAI Locator Healing - Summary Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")

            if report:
                f.write(f"Total Healings: {len(report)}\n\n")

                for i, entry in enumerate(report, 1):
                    f.write(f"[{i}] {entry['locator_name']}\n")
                    f.write(f"    Page: {entry['page']}\n")
                    f.write(f"    Old: {entry['old_by']} = {entry['old_value']}\n")
                    f.write(f"    New: {entry['new_by']} = {entry['new_value']}\n")
                    f.write(f"    Confidence: {entry['confidence']}\n")
                    f.write(f"    Reasoning: {entry['reasoning']}\n")
                    f.write(f"    Time: {entry['timestamp']}\n\n")
            else:
                f.write("No healings occurred - all locators stable!\n")

        print(f"✅ Summary text report: {txt_file}")

        # Export as CSV
        csv_file = os.path.join(report_dir, f"healing_data_{timestamp}.csv")
        with open(csv_file, 'w') as f:
            # Header
            f.write("Locator,Page,Old Strategy,Old Value,New Strategy,New Value,Confidence,Timestamp\n")

            # Data
            for entry in report:
                f.write(f'"{entry["locator_name"]}",')
                f.write(f'"{entry["page"]}",')
                f.write(f'"{entry["old_by"]}",')
                f.write(f'"{entry["old_value"]}",')
                f.write(f'"{entry["new_by"]}",')
                f.write(f'"{entry["new_value"]}",')
                f.write(f'"{entry["confidence"]}",')
                f.write(f'"{entry["timestamp"]}"\n')

        print(f"✅ CSV data export: {csv_file}")

        print(f"\n📁 All reports saved to: {report_dir}/")
        print("\n✅ TEST PASSED: Export completed successfully!")

    @pytest.mark.healing
    def test_healing_recommendations(self, smart_finder, locator_registry):
        """Generate recommendations based on healing patterns"""
        print("\n" + "=" * 70)
        print("🧪 TEST: Healing Recommendations")
        print("=" * 70)

        report = smart_finder.get_healing_report()
        all_locators = locator_registry.get_all_locators()

        print("\n💡 RECOMMENDATIONS")
        print("=" * 70)

        if not report:
            print("\n✅ No healings needed - your locators are stable!")
            print("   Keep maintaining good locator practices.")
        else:
            recommendations = []

            # Check for low confidence healings
            low_confidence = [r for r in report if r['confidence'] == 'low']
            if low_confidence:
                recommendations.append(
                    f"⚠️  {len(low_confidence)} low-confidence healing(s) detected. "
                    f"Consider manually reviewing these locators."
                )

            # Check for repeated strategy patterns
            xpath_to_css = sum(1 for r in report if r['old_by'] == 'XPATH' and r['new_by'] == 'CSS_SELECTOR')
            if xpath_to_css > 1:
                recommendations.append(
                    f"💡 {xpath_to_css} XPath locators were replaced with CSS. "
                    f"Consider using CSS selectors from the start for better stability."
                )

            # Check for ID migrations
            id_changes = sum(1 for r in report if r['old_by'] == 'ID')
            if id_changes > 0:
                recommendations.append(
                    f"⚠️  {id_changes} ID-based locator(s) changed. "
                    f"Work with developers to ensure stable IDs or use data-testid attributes."
                )

            # Check for high failure counts
            high_failure_locators = [
                (name, loc) for name, loc in all_locators.items()
                if loc.failure_count > 2
            ]
            if high_failure_locators:
                recommendations.append(
                    f"🔴 {len(high_failure_locators)} locator(s) have >2 failures. "
                    f"These may need manual attention or better strategies."
                )

            # Display recommendations
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    print(f"\n{i}. {rec}")
            else:
                print("\n✅ No specific recommendations - healings were successful!")

            # General best practices
            print("\n📚 BEST PRACTICES")
            print("=" * 70)
            print("  1. Prefer ID and Name attributes when available")
            print("  2. Use data-testid or data-qa attributes for test stability")
            print("  3. Avoid absolute XPath; use relative XPath when needed")
            print("  4. Keep locator descriptions clear for better GenAI suggestions")
            print("  5. Regularly review and update locators based on healing patterns")

        print("\n✅ TEST PASSED: Recommendations generated!")


if __name__ == "__main__":
    """Allow running this test file directly"""
    pytest.main([__file__, "-v", "-s", "-m", "healing"])