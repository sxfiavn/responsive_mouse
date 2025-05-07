
import time
from model.stress_model import run_model  # TODO: Imported from stress_model.py
from config import INTERVENTION_INTERVAL_SEC

def start_monitoring(buffer, ui_reference, on_stress_callback, should_continue_fn, interval=10):
    import logging
    logging.info("Stress monitoring started")

    while should_continue_fn():
        try:
            time.sleep(interval)
            now = time.time()

            # Optional: bail early after sleep, in case we were stopped during sleep
            if not should_continue_fn():
                print("Skipping result: user exited before inference finished")
                break

            recent_data = [
                (ppg, gsr, t) for (ppg, gsr, t) in list(buffer)
                if now - t <= interval
            ]

            if len(recent_data) < 250:
                continue

            result = run_model(recent_data)

            # Check again here — ignore result if user navigated away
            if not should_continue_fn():
                print("Skipping result: user exited before inference finished")
                logging.info("Skipping result: user exited before inference finished")
                break

            if result == "stressed":
                print("Stress detected!")
                logging.info("Stress detected! Triggering intervention.")

                current_time = time.time()
                last_trigger = getattr(ui_reference, "last_intervention_time", 0)

                if current_time - last_trigger >= INTERVENTION_INTERVAL_SEC: 
                    logging.info("Enough time passed. Triggering intervention.")
                    ui_reference.after(0, on_stress_callback)
                else:
                    print("Too soon for another intervention.")
                    logging.info("Too soon for another intervention.")

        except Exception as e:
            print(f"[Monitor Error] {e}")
            logging.error(f"[Monitor Error] {e}")
            break

    logging.info("Monitoring thread exited.")

