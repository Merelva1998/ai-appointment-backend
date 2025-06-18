#!/usr/bin/env python3
"""
Web dashboard for viewing and managing appointments
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
import os
import json
from ai_appointment_agent.appointment_manager import AppointmentManager
from ai_appointment_agent.logger import Logger
from ai_appointment_agent.user_manager import UserManager

app = Flask(__name__)
logger = Logger("dashboard.log")

# Initialize managers
appointment_manager = AppointmentManager()
user_manager = UserManager()


@app.route('/')
def dashboard():
    try:
        upcoming = appointment_manager.get_upcoming_appointments(14)
        today = datetime.now()
        todays_appointments = appointment_manager.get_daily_schedule(today)
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        week_appointments = appointment_manager.get_appointments_for_period(
            week_start, week_end)
        return render_template('dashboard.html',
                               upcoming=upcoming,
                               today=todays_appointments,
                               week=week_appointments,
                               current_date=today)
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        return f"Error loading dashboard: {str(e)}", 500


@app.route('/settings')
def settings():
    try:
        all_appointments = appointment_manager.appointments
        total_appointments = len(all_appointments)
        scheduled_appointments = len(
            [a for a in all_appointments if a['status'] == 'scheduled'])
        cancelled_appointments = len(
            [a for a in all_appointments if a['status'] == 'cancelled'])

        with open("user_settings.json", "r") as f:
            user_settings = json.load(f)

        return render_template(
            'settings.html',
            total_appointments=total_appointments,
            scheduled_appointments=scheduled_appointments,
            cancelled_appointments=cancelled_appointments,
            user_settings=user_settings,
            subscription_active=user_manager.is_subscription_active())
    except Exception as e:
        return f"Fout bij laden van instellingen: {str(e)}", 500


@app.route('/update-settings', methods=['POST'])
def update_settings():
    try:
        with open("user_settings.json", "r") as f:
            settings = json.load(f)

        settings[
            "require_confirmation"] = "require_confirmation" in request.form
        settings["notify_email"] = "notify_email" in request.form
        settings["notify_popup"] = "notify_popup" in request.form
        settings["notify_sms"] = "notify_sms" in request.form

        with open("user_settings.json", "w") as f:
            json.dump(settings, f, indent=2)

        return redirect("/settings")
    except Exception as e:
        return f"Fout bij opslaan van instellingen: {str(e)}", 500


# Andere routes kun je eventueel later weer toevoegen als je die nodig hebt (zoals /api/appointments etc.)

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
