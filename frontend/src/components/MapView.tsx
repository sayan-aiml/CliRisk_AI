import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { MapContainer, TileLayer, useMapEvents, Marker, Popup, ZoomControl } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { FiMapPin, FiInfo, FiLayers, FiMap } from 'react-icons/fi';
import climateRiskApi, { RiskScoreResponse } from '../services/climateRiskApi';

// Fix Leaflet marker icon issue
const markerIcon = require('leaflet/dist/images/marker-icon.png');
const markerIconRetina = require('leaflet/dist/images/marker-icon-2x.png');
const markerShadow = require('leaflet/dist/images/marker-shadow.png');

const DefaultIcon = L.icon({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIconRetina,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

const MapWrapper = styled.div`
  flex: 1;
  display: flex;
  position: relative;
  height: 100%;
  
  .leaflet-container {
    width: 100%;
    height: 100%;
    background: #0b1426;
  }
`;

const MapControls = styled.div`
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 1000; // Above leaflet
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const LeftControls = styled.div`
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const ControlPanel = styled.div`
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  padding: 1.5rem;
  width: 300px;
  box-shadow: var(--shadow-glow);
`;

const ControlTitle = styled.h3`
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-light);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const LocationInfo = styled.div`
  background: var(--secondary-dark);
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
  border: 1px solid var(--glass-border);
`;

const InfoRow = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  
  &:last-child {
    margin-bottom: 0;
  }
`;

const Label = styled.span`
  color: var(--text-muted);
`;

const Value = styled.span`
  color: var(--text-light);
  font-weight: 500;
`;

const RiskIndicator = styled.div<{ $riskLevel: string }>`
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-align: center;
  background: ${props => {
    switch (props.$riskLevel) {
      case 'low': return 'var(--success-green)';
      case 'moderate': return 'var(--warning-orange)';
      case 'high': return 'var(--danger-red)';
      case 'severe': return '#ff0000';
      default: return 'var(--text-muted)';
    }
  }};
  color: ${props => props.$riskLevel === 'severe' ? 'white' : 'var(--primary-dark)'};
`;

function MapEvents({ onMapClick }: { onMapClick: (lat: number, lng: number) => void }) {
  useMapEvents({
    click: (e) => {
      onMapClick(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
}

function MapView() {
  const [mapCenter, setMapCenter] = useState<[number, number]>([20, 0]); // Default global view
  const [zoom, setZoom] = useState(2);
  const [selectedLocation, setSelectedLocation] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Auto-center on user GPS on mount
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setMapCenter([latitude, longitude]);
          setZoom(10);
        },
        (error) => {
          console.warn("Geolocation denied or failed:", error.message);
          // Keep default center
        }
      );
    }
  }, []);

  const determineRiskLevel = (score: number) => {
    if (score < 25) return 'low';
    if (score < 50) return 'moderate';
    if (score < 75) return 'high';
    return 'severe';
  };

  const handleMapClick = async (lat: number, lng: number) => {
    setIsLoading(true);
    setError(null);

    try {
      const riskData = await climateRiskApi.getRiskScore({
        latitude: lat,
        longitude: lng,
        temperature_increase: 2.0,
        precipitation_change: 10.0
      });

      setSelectedLocation({
        longitude: lng,
        latitude: lat,
        compositeScore: riskData.composite_risk_score,
        riskCategory: riskData.risk_category,
        floodRisk: riskData.flood_risk_score,
        heatRisk: riskData.heat_risk_score,
        airQualityRisk: riskData.air_quality_risk_score,
        expectedAnnualLoss: 0,
        confidence: riskData.confidence_score
      });

      const financialData = await climateRiskApi.getFinancialLoss({
        property_value: 500000,
        property_type: 'residential',
        risk_assessment: riskData
      });

      setSelectedLocation((prev: any) => {
        const updated = {
          ...prev,
          expectedAnnualLoss: financialData.expected_annual_loss,
          financialData
        };
        localStorage.setItem('lastAssessment', JSON.stringify(updated));
        return updated;
      });

    } catch (err: any) {
      console.error("Failed to fetch risk data:", err);
      setError("Failed to fetch climate risk data. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <MapWrapper>
      <MapContainer
        center={mapCenter}
        zoom={zoom}
        zoomControl={false}
        minZoom={2}
        maxBounds={[[-90, -180], [90, 180]]}
        maxBoundsViscosity={1.0}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png"
          noWrap={true}
          bounds={[[-90, -180], [90, 180]]}
        />
        <ZoomControl position="topright" />
        <MapEvents onMapClick={handleMapClick} />
        {selectedLocation && (
          <Marker position={[selectedLocation.latitude, selectedLocation.longitude]} icon={DefaultIcon}>
            <Popup>
              <div style={{ color: '#000' }}>
                <strong>Risk Score: {selectedLocation.compositeScore}</strong><br />
                Category: {selectedLocation.riskCategory}
              </div>
            </Popup>
          </Marker>
        )}
      </MapContainer>

      <LeftControls>
        <ControlPanel>
          <ControlTitle>
            <FiMap />
            ClimateRisk Map
          </ControlTitle>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1rem' }}>
            Professional climate risk assessments using **Open-Meteo Public Data**.
            Includes **ERA5** historical benchmarks and **CMIP6** (IPCC-grade) projections.
          </p>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.75rem', borderLeft: '2px solid var(--accent-purple)', paddingLeft: '8px' }}>
            No private API keys required. All data is sourced from global scientific open-data initiatives.
          </p>

          {selectedLocation && (
            <LocationInfo>
              <ControlTitle>
                <FiMapPin />
                Location Risk
              </ControlTitle>

              <InfoRow>
                <Label>Coordinates:</Label>
                <Value>{selectedLocation.latitude.toFixed(4)}, {selectedLocation.longitude.toFixed(4)}</Value>
              </InfoRow>

              <InfoRow>
                <Label>Risk Score:</Label>
                <Value>{selectedLocation.compositeScore}/100</Value>
              </InfoRow>

              <InfoRow>
                <Label>Risk Category:</Label>
                <RiskIndicator $riskLevel={determineRiskLevel(selectedLocation.compositeScore)}>
                  {selectedLocation.riskCategory}
                </RiskIndicator>
              </InfoRow>

              <InfoRow>
                <Label>Flood Risk:</Label>
                <Value>{selectedLocation.floodRisk}/100</Value>
              </InfoRow>

              <InfoRow>
                <Label>Heat Risk:</Label>
                <Value>{selectedLocation.heatRisk}/100</Value>
              </InfoRow>

              <InfoRow>
                <Label>Air Quality:</Label>
                <Value>{selectedLocation.airQualityRisk}/100</Value>
              </InfoRow>

              <InfoRow>
                <Label>Expected Annual Loss:</Label>
                <Value>${selectedLocation.expectedAnnualLoss.toLocaleString()}</Value>
              </InfoRow>

              <InfoRow>
                <Label>Confidence:</Label>
                <Value>{selectedLocation.confidence.toFixed(1)}%</Value>
              </InfoRow>
            </LocationInfo>
          )}

          {isLoading && (
            <div style={{ display: 'flex', justifyContent: 'center', marginTop: '1rem' }}>
              <div className="spinner"></div>
            </div>
          )}

          {error && (
            <div style={{ color: 'var(--danger-red)', marginTop: '1rem', fontSize: '0.9rem' }}>
              {error}
            </div>
          )}

          {!selectedLocation && (
            <div style={{ marginTop: '1rem' }}>
              <ControlTitle>
                <FiInfo />
                Instructions
              </ControlTitle>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: '1.5' }}>
                Click anywhere on the map to calculate climate risk for that location.
              </p>
            </div>
          )}
        </ControlPanel>
      </LeftControls>
    </MapWrapper>
  );
}

export default MapView;