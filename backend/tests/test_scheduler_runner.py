from app.scheduler.runner import SchedulerRunner


def test_scheduler_reads_intervals_from_app_settings(session) -> None:
    runner = SchedulerRunner(session=session)

    plan = runner.build_plan()

    assert plan.sync_interval_minutes == 60
    assert plan.analysis_interval_minutes == 240
