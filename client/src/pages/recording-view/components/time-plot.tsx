import Plot from 'react-plotly.js';
import React, { useEffect, useState } from 'react';
import { template } from '@/utils/plotlyTemplate';
import { useSpectrogramContext } from '../hooks/use-spectrogram-context';
import { useCursorContext } from '../hooks/use-cursor-context';

interface TimePlotProps {
  displayedIQ: Float32Array;
  fftStepSize: Number;
}

export const TimePlot = ({ displayedIQ, fftStepSize }: TimePlotProps) => {
  const { spectrogramWidth, spectrogramHeight, freqShift } = useSpectrogramContext();
  const { cursorFreqShift } = useCursorContext(); // cursorFreqShift is in normalized freq (-0.5 to +0.5) regardless of if display RF is on
  const [I, setI] = useState<Float32Array>();
  const [Q, setQ] = useState<Float32Array>();
  const [isLoading, setIsLoading] = useState(true);
  
  // Track if we currently have valid data loaded (prevents Plot rendering before/without data)
  // Note: This flag is reset to false when data becomes invalid or empty
  const hasEverHadData = React.useRef(false);

  useEffect(() => {
    console.log('[TimePlot] useEffect triggered', {
      hasDisplayedIQ: !!displayedIQ,
      displayedIQLength: displayedIQ?.length,
      fftStepSize: fftStepSize,
      isLoading,
      hasEverHadData: hasEverHadData.current,
      freqShift,
      cursorFreqShift,
    });

    if (displayedIQ && displayedIQ.length > 0) {
      // Check if displayedIQ contains valid data (not all -Infinity)
      // For performance, only check a sample of values
      const sampleSize = Math.min(100, displayedIQ.length);
      const hasValidData = Array.from(displayedIQ.slice(0, sampleSize)).some((val) => val !== -Infinity && !isNaN(val));
      
      console.log('[TimePlot] Data validation', {
        sampleSize,
        hasValidData,
        firstFewValues: Array.from(displayedIQ.slice(0, 10)),
      });
      
      if (!hasValidData) {
        console.log('[TimePlot] Invalid data detected, staying in loading state');
        setIsLoading(true);
        hasEverHadData.current = false; // Reset flag when data becomes invalid
        return;
      }

      console.log('[TimePlot] Processing valid data...');
      const temp_I = new Float32Array(displayedIQ.length / 2);
      const temp_Q = new Float32Array(displayedIQ.length / 2);
      for (let i = 0; i < displayedIQ.length / 2; i++) {
        if (freqShift) {
          // Multiplying two complex numbers: (a + ib)(c + id) = (ac - bd) + i(ad + bc).
          temp_I[i] =
            displayedIQ[i * 2] * Math.cos(-2 * Math.PI * cursorFreqShift * i) -
            displayedIQ[i * 2 + 1] * Math.sin(-2 * Math.PI * cursorFreqShift * i);
          temp_Q[i] =
            displayedIQ[i * 2] * Math.sin(-2 * Math.PI * cursorFreqShift * i) +
            displayedIQ[i * 2 + 1] * Math.cos(-2 * Math.PI * cursorFreqShift * i);
        } else {
          temp_I[i] = displayedIQ[i * 2];
          temp_Q[i] = displayedIQ[i * 2 + 1];
        }
      }
      setI(temp_I);
      setQ(temp_Q);
      
      console.log('[TimePlot] Data processed successfully', {
        ILength: temp_I.length,
        QLength: temp_Q.length,
      });
      
      hasEverHadData.current = true; // Mark that we've successfully loaded data
      setIsLoading(false);
      console.log('[TimePlot] State updated: isLoading=false, hasEverHadData=true');
    } else {
      console.log('[TimePlot] No data or empty data, staying in loading state');
      setIsLoading(true);
      hasEverHadData.current = false; // Reset flag when no data
    }
  }, [displayedIQ, freqShift, cursorFreqShift]);

  return (
    <div className="px-3">
      <p className="text-primary text-center">
        Below shows the time domain of the sample range displayed on the spectrogram tab
      </p>
      {(() => {
        console.log('[TimePlot] Render decision', {
          fftStepSize,
          isLoading,
          hasEverHadData: hasEverHadData.current,
          hasI: !!I,
          ILength: I?.length,
          hasQ: !!Q,
          QLength: Q?.length,
        });
        
        if (fftStepSize !== 0) {
          console.log('[TimePlot] fftStepSize is not 0, showing message');
          return (
            <>
              <h1 className="text-center">Plot only visible when Zoom Out Level is minimum (0)</h1>
              <p className="text-primary text-center mb-6">(Otherwise the IQ samples are not contiguous)</p>
            </>
          );
        }
        
        const shouldRender = !isLoading && hasEverHadData.current && I && Q && I.length > 0 && Q.length > 0;
        console.log('[TimePlot] Should render plot?', shouldRender);
        
        if (!shouldRender) {
          return (
            <div className="flex justify-center items-center" style={{ height: spectrogramHeight }}>
              <p className="text-primary text-center">Loading time domain data...</p>
            </div>
          );
        }
        
        // Use scatter (SVG) instead of scattergl (WebGL) to avoid WebGL buffer issues
        // scattergl was causing "clear() called with no buffers" errors for certain data sizes
        const plotType = 'scatter';
        console.log('[TimePlot] Using plot type:', plotType, 'for data length:', I.length);
        
        return (
          <Plot
            data={[
              {
                y: I,
                type: plotType,
                name: 'I',
              },
              {
                y: Q,
                type: plotType,
                name: 'Q',
              },
            ]}
            layout={{
              width: spectrogramWidth,
              height: spectrogramHeight,
              margin: {
                l: 60,
                r: 20,
                b: 50,
                t: 20,
                pad: 4,
              },
              dragmode: 'pan',
              showlegend: true,
              template: template,
              xaxis: {
                title: 'Time',
                autorange: true,
                rangeslider: {
                  visible: true,
                  autorange: true,
                },
              },
              yaxis: {
                title: 'Samples',
                autorange: true,
                fixedrange: false,
              },
              uirevision: 'true', // keeps zoom/pan the same when data changes
            }}
            config={{
              displayModeBar: true,
              scrollZoom: true,
            }}
          />
        );
      })()}
    </div>
  );
};
