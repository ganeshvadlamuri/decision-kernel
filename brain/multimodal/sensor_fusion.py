"""Sensor fusion - Combine vision + audio + touch."""

from typing import Any


class SensorFusion:
    """Combine vision + audio + touch."""

    def fuse(self, vision: dict[str, Any], audio: dict[str, Any], touch: dict[str, Any]) -> dict[str, Any]:
        """Fuse multiple sensor modalities."""
        fused: dict[str, Any] = {
            "confidence": 0.0,
            "object_detected": False,
            "object_properties": {},
        }

        # Combine evidence from multiple sensors
        evidence_count = 0
        total_confidence = 0.0

        if vision.get("object_detected"):
            evidence_count += 1
            total_confidence += vision.get("confidence", 0.5)
            vision_properties = vision.get("properties", {})
            if isinstance(vision_properties, dict):
                fused["object_properties"].update(vision_properties)

        if audio.get("sound_detected"):
            evidence_count += 1
            total_confidence += audio.get("confidence", 0.5)

        if touch.get("contact_detected"):
            evidence_count += 1
            total_confidence += touch.get("confidence", 0.5)

        if evidence_count > 0:
            fused["confidence"] = total_confidence / evidence_count
            fused["object_detected"] = evidence_count >= 2  # Require 2+ sensors

        return fused
