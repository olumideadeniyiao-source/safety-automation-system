import datetime
from typing import Dict, List, Optional, Tuple
import uuid

class SafetySuperintendentSystem:
    def __init__(self):
        # Sites: {site_id: {"name": str, "location": str, "status": str, "hazards": List[Dict]}}
        self.sites: Dict[str, Dict] = {}

        # Inspections: {inspection_id: {"site_id": str, "date": str, "inspector": str, "findings": List[Dict], "status": str}}
        self.inspections: Dict[str, Dict] = {}

        # Hazards: {hazard_id: {"site_id": str, "type": str, "severity": str, "status": str, "mitigation": str}}
        self.hazards: Dict[str, Dict] = {}

        # HSE Reports: {report_id: {"period": str, "metrics": Dict, "site_id": str, "status": str}}
        self.hse_reports: Dict[str, Dict] = {}

        # Audits: {audit_id: {"site_id": str, "type": str, "date": str, "findings": List[Dict], "status": str}}
        self.audits: Dict[str, Dict] = {}

        # Incidents: {incident_id: {"site_id": str, "type": str, "date": str, "severity": str, "investigation": Dict, "status": str}}
        self.incidents: Dict[str, Dict] = {}

        # Safety Measures: {measure_id: {"site_id": str, "description": str, "implementation_date": str, "status": str}}
        self.safety_measures: Dict[str, Dict] = {}

        # Audit Logs: List[Dict]
        self.audit_logs: List[Dict] = {}

    # --- Site Management ---
    def add_site(self, name: str, location: str) -> str:
        """Add a new construction site."""
        site_id = f"SITE{str(uuid.uuid4())[:6]}"
        self.sites[site_id] = {
            "name": name,
            "location": location,
            "status": "Active",
            "hazards": []
        }
        self._log_activity("site_added", {"site_id": site_id, "name": name, "location": location})
        return f"Site '{name}' added with ID: {site_id}"

    def update_site_status(self, site_id: str, status: str) -> str:
        """Update the status of a site (e.g., Active, Inactive, Under Review)."""
        if site_id in self.sites:
            self.sites[site_id]["status"] = status
            self._log_activity("site_status_updated", {"site_id": site_id, "status": status})
            return f"Site {site_id} status updated to: {status}"
        return f"Site ID {site_id} not found."

    # --- Site Inspections ---
    def conduct_inspection(self, site_id: str, inspector: str, findings: List[Dict]) -> str:
        """Conduct a site inspection and record findings."""
        if site_id in self.sites:
            inspection_id = f"INSP{str(uuid.uuid4())[:6]}"
            self.inspections[inspection_id] = {
                "site_id": site_id,
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "inspector": inspector,
                "findings": findings,
                "status": "Completed"
            }
            # Add findings as hazards to the site
            for finding in findings:
                hazard_id = f"HAZ{str(uuid.uuid4())[:6]}"
                self.hazards[hazard_id] = {
                    "site_id": site_id,
                    "type": finding["type"],
                    "severity": finding["severity"],
                    "status": "Identified",
                    "mitigation": finding.get("mitigation", "")
                }
                self.sites[site_id]["hazards"].append(hazard_id)
            self._log_activity("inspection_conducted", {"inspection_id": inspection_id, "site_id": site_id})
            return f"Inspection conducted with ID: {inspection_id}"
        return f"Site ID {site_id} not found."

    def get_inspection_report(self, inspection_id: str) -> Optional[Dict]:
        """Retrieve an inspection report by ID."""
        return self.inspections.get(inspection_id)

    # --- Hazard Management ---
    def add_hazard(self, site_id: str, hazard_type: str, severity: str, mitigation: str = "") -> str:
        """Add a hazard to a site."""
        if site_id in self.sites:
            hazard_id = f"HAZ{str(uuid.uuid4())[:6]}"
            self.hazards[hazard_id] = {
                "site_id": site_id,
                "type": hazard_type,
                "severity": severity,
                "status": "Identified",
                "mitigation": mitigation
            }
            self.sites[site_id]["hazards"].append(hazard_id)
            self._log_activity("hazard_added", {"hazard_id": hazard_id, "site_id": site_id, "type": hazard_type})
            return f"Hazard '{hazard_type}' added with ID: {hazard_id}"
        return f"Site ID {site_id} not found."

    def mitigate_hazard(self, hazard_id: str, mitigation: str) -> str:
        """Update the mitigation status of a hazard."""
        if hazard_id in self.hazards:
            self.hazards[hazard_id]["status"] = "Mitigated"
            self.hazards[hazard_id]["mitigation"] = mitigation
            self._log_activity("hazard_mitigated", {"hazard_id": hazard_id, "mitigation": mitigation})
            return f"Hazard {hazard_id} mitigated with: {mitigation}"
        return f"Hazard ID {hazard_id} not found."

    # --- HSE Performance Reports ---
    def generate_hse_report(self, site_id: str, period: str, metrics: Dict) -> str:
        """Generate an HSE (Health, Safety, Environment) performance report."""
        if site_id in self.sites:
            report_id = f"HSE{str(uuid.uuid4())[:6]}"
            self.hse_reports[report_id] = {
                "period": period,
                "metrics": metrics,
                "site_id": site_id,
                "status": "Generated"
            }
            self._log_activity("hse_report_generated", {"report_id": report_id, "site_id": site_id, "period": period})
            return f"HSE Report generated for {period} with ID: {report_id}"
        return f"Site ID {site_id} not found."

    def get_hse_report(self, report_id: str) -> Optional[Dict]:
        """Retrieve an HSE report by ID."""
        return self.hse_reports.get(report_id)

    # --- Safety Audits ---
    def conduct_audit(self, site_id: str, audit_type: str, findings: List[Dict]) -> str:
        """Conduct an internal or external safety audit."""
        if site_id in self.sites:
            audit_id = f"AUD{str(uuid.uuid4())[:6]}"
            self.audits[audit_id] = {
                "site_id": site_id,
                "type": audit_type,
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "findings": findings,
                "status": "Completed"
            }
            self._log_activity("audit_conducted", {"audit_id": audit_id, "site_id": site_id, "type": audit_type})
            return f"Audit conducted with ID: {audit_id}"
        return f"Site ID {site_id} not found."

    def get_audit_report(self, audit_id: str) -> Optional[Dict]:
        """Retrieve an audit report by ID."""
        return self.audits.get(audit_id)

    # --- Incident Management ---
    def report_incident(self, site_id: str, incident_type: str, severity: str, description: str) -> str:
        """Report a workplace incident."""
        if site_id in self.sites:
            incident_id = f"INC{str(uuid.uuid4())[:6]}"
            self.incidents[incident_id] = {
                "site_id": site_id,
                "type": incident_type,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "severity": severity,
                "description": description,
                "investigation": {
                    "status": "Open",
                    "findings": [],
                    "recommendations": []
                },
                "status": "Reported"
            }
            self._log_activity("incident_reported", {"incident_id": incident_id, "site_id": site_id, "type": incident_type})
            return f"Incident reported with ID: {incident_id}"
        return f"Site ID {site_id} not found."

    def investigate_incident(self, incident_id: str, findings: List[str], recommendations: List[str]) -> str:
        """Investigate an incident and add findings/recommendations."""
        if incident_id in self.incidents:
            self.incidents[incident_id]["investigation"]["status"] = "Closed"
            self.incidents[incident_id]["investigation"]["findings"] = findings
            self.incidents[incident_id]["investigation"]["recommendations"] = recommendations
            self.incidents[incident_id]["status"] = "Investigated"
            self._log_activity("incident_investigated", {"incident_id": incident_id, "findings": findings})
            return f"Incident {incident_id} investigated. Recommendations: {recommendations}"
        return f"Incident ID {incident_id} not found."

    # --- Safety Measures ---
    def implement_safety_measure(self, site_id: str, description: str) -> str:
        """Implement a preventive safety measure at a site."""
        if site_id in self.sites:
            measure_id = f"SM{str(uuid.uuid4())[:6]}"
            self.safety_measures[measure_id] = {
                "site_id": site_id,
                "description": description,
                "implementation_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "status": "Implemented"
            }
            self._log_activity("safety_measure_implemented", {"measure_id": measure_id, "site_id": site_id, "description": description})
            return f"Safety measure implemented with ID: {measure_id}"
        return f"Site ID {site_id} not found."

    # --- Audit Logging ---
    def _log_activity(self, action: str, details: Dict) -> None:
        """Log an activity to the audit trail."""
        log_entry = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "details": details
        }
        self.audit_logs.append(log_entry)

    def get_audit_logs(self) -> List[Dict]:
        """Retrieve all audit logs."""
        return self.audit_logs

    # --- Reporting ---
    def generate_safety_report(self, site_id: str) -> Dict:
        """Generate a comprehensive safety report for a site."""
        if site_id in self.sites:
            site = self.sites[site_id]
            report = {
                "site_id": site_id,
                "name": site["name"],
                "location": site["location"],
                "status": site["status"],
                "hazards": [self.hazards[hazard_id] for hazard_id in site["hazards"]],
                "inspections": [insp for insp in self.inspections.values() if insp["site_id"] == site_id],
                "audits": [audit for audit in self.audits.values() if audit["site_id"] == site_id],
                "incidents": [inc for inc in self.incidents.values() if inc["site_id"] == site_id],
                "safety_measures": [sm for sm in self.safety_measures.values() if sm["site_id"] == site_id],
                "hse_reports": [hse for hse in self.hse_reports.values() if hse["site_id"] == site_id]
            }
            return report
        return {"error": "Site ID not found"}

    def generate_summary_report(self) -> Dict:
        """Generate a summary report across all sites."""
        total_sites = len(self.sites)
        total_hazards = len(self.hazards)
        total_inspections = len(self.inspections)
        total_audits = len(self.audits)
        total_incidents = len(self.incidents)
        total_safety_measures = len(self.safety_measures)

        return {
            "total_sites": total_sites,
            "total_hazards": total_hazards,
            "total_inspections": total_inspections,
            "total_audits": total_audits,
            "total_incidents": total_incidents,
            "total_safety_measures": total_safety_measures,
            "hazard_severity_distribution": self._calculate_hazard_severity_distribution(),
            "incident_severity_distribution": self._calculate_incident_severity_distribution()
        }

    def _calculate_hazard_severity_distribution(self) -> Dict:
        """Calculate the distribution of hazard severities."""
        severity_counts = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
        for hazard in self.hazards.values():
            severity = hazard["severity"]
            if severity in severity_counts:
                severity_counts[severity] += 1
        return severity_counts

    def _calculate_incident_severity_distribution(self) -> Dict:
        """Calculate the distribution of incident severities."""
        severity_counts = {"Minor": 0, "Moderate": 0, "Major": 0, "Critical": 0}
        for incident in self.incidents.values():
            severity = incident["severity"]
            if severity in severity_counts:
                severity_counts[severity] += 1
        return severity_counts

# --- Example Usage ---
if __name__ == "__main__":
    safety_system = SafetySuperintendentSystem()

    # Add construction sites
    print("=== Site Management ===")
    print(safety_system.add_site("Drilling Rig Alpha", "Freetown, Sierra Leone"))
    print(safety_system.add_site("Construction Site Beta", "Bo, Sierra Leone"))

    # Conduct site inspections
    print("\n=== Site Inspections ===")
    findings = [
        {"type": "Electrical Hazard", "severity": "High", "mitigation": "Isolate and repair wiring"},
        {"type": "Fire Risk", "severity": "Critical", "mitigation": "Install fire suppression systems"}
    ]
    print(safety_system.conduct_inspection("SITE1", "John Doe", findings))

    # Add and mitigate hazards
    print("\n=== Hazard Management ===")
    print(safety_system.add_hazard("SITE1", "Falling Objects", "Medium", "Use hard hats and safety nets"))
    print(safety_system.mitigate_hazard("HAZ1", "Installed safety nets and enforced PPE"))

    # Generate HSE reports
    print("\n=== HSE Performance Reports ===")
    metrics = {
        "incident_rate": 0.5,
        "hazard_resolution_rate": 0.9,
        "compliance_score": 0.95
    }
    print(safety_system.generate_hse_report("SITE1", "Q1 2026", metrics))

    # Conduct safety audits
    print("\n=== Safety Audits ===")
    audit_findings = [
        {"type": "PPE Compliance", "status": "Non-Compliant", "action": "Retrain staff"},
        {"type": "Emergency Exits", "status": "Compliant", "action": "None"}
    ]
    print(safety_system.conduct_audit("SITE1", "Internal", audit_findings))

    # Report and investigate incidents
    print("\n=== Incident Management ===")
    print(safety_system.report_incident("SITE1", "Fire", "Critical", "Fire broke out near drilling equipment"))
    print(safety_system.investigate_incident(
        "INC1",
        ["Faulty wiring identified", "Lack of fire suppression"],
        ["Replace wiring", "Install fire suppression systems", "Conduct fire drills"]
    ))

    # Implement safety measures
    print("\n=== Safety Measures ===")
    print(safety_system.implement_safety_measure("SITE1", "Install fire suppression systems"))
    print(safety_system.implement_safety_measure("SITE1", "Conduct weekly fire drills"))

    # Generate reports
    print("\n=== Safety Report for Site 1 ===")
    site_report = safety_system.generate_safety_report("SITE1")
    for key, value in site_report.items():
        print(f"{key}: {value}")

    print("\n=== Summary Report ===")
    summary_report = safety_system.generate_summary_report()
    for key, value in summary_report.items():
        print(f"{key}: {value}")
