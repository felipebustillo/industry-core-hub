/********************************************************************************
 * Eclipse Tractus-X - Industry Core Hub Frontend
 *
 * Copyright (c) 2025 Contributors to the Eclipse Foundation
 *
 * See the NOTICE file(s) distributed with this work for additional
 * information regarding copyright ownership.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Apache License, Version 2.0 which is available at
 * https://www.apache.org/licenses/LICENSE-2.0.
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied. See the
 * License for the specific language govern in permissions and limitations
 * under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
 ********************************************************************************/

import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid2,
  Typography,
  Box,
  SelectChangeEvent
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { CertificateFormData, UploadCertificateDialogProps } from '../../types/dialog-types';
import { certificateManagementConfig } from '../../config';

const initialFormData: CertificateFormData = {
  name: '',
  type: '',
  bpn: '',
  issuer: '',
  validFrom: '',
  validUntil: '',
  description: '',
  document: undefined
};

// Max file size: 10MB
const MAX_FILE_SIZE = 10 * 1024 * 1024;
const ALLOWED_FILE_TYPES = ['application/pdf', 'image/png', 'image/jpeg'];

export const UploadCertificateDialog = ({
  open,
  onClose,
  onSave,
  certificateData
}: UploadCertificateDialogProps) => {
  const [formData, setFormData] = useState<CertificateFormData>(initialFormData);
  const [errors, setErrors] = useState<Partial<Record<keyof CertificateFormData | 'document', string>>>({});
  const [fileError, setFileError] = useState<string | null>(null);

  useEffect(() => {
    if (certificateData) {
      setFormData(certificateData);
    } else {
      setFormData(initialFormData);
    }
    setErrors({});
    setFileError(null);
  }, [certificateData, open]);

  const handleChange = (field: keyof CertificateFormData) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData(prev => ({ ...prev, [field]: event.target.value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const handleSelectChange = (field: keyof CertificateFormData) => (
    event: SelectChangeEvent
  ) => {
    setFormData(prev => ({ ...prev, [field]: event.target.value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setFileError(null);
    
    if (file) {
      // Validate file type
      if (!ALLOWED_FILE_TYPES.includes(file.type)) {
        setFileError('Invalid file type. Please upload a PDF, PNG, or JPG file.');
        return;
      }
      
      // Validate file size
      if (file.size > MAX_FILE_SIZE) {
        setFileError('File size exceeds 10MB limit.');
        return;
      }
      
      setFormData(prev => ({ ...prev, document: file }));
    }
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof CertificateFormData, string>> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Certificate name is required';
    }
    if (!formData.type) {
      newErrors.type = 'Certificate type is required';
    }
    if (!formData.bpn.trim()) {
      newErrors.bpn = 'BPN is required';
    } else if (!certificateManagementConfig.validation.bpn.pattern.test(formData.bpn)) {
      newErrors.bpn = certificateManagementConfig.validation.bpn.errorMessage;
    }
    if (!formData.issuer.trim()) {
      newErrors.issuer = 'Issuer is required';
    }
    if (!formData.validFrom) {
      newErrors.validFrom = 'Valid from date is required';
    }
    if (!formData.validUntil) {
      newErrors.validUntil = 'Valid until date is required';
    }
    if (formData.validFrom && formData.validUntil && new Date(formData.validFrom) >= new Date(formData.validUntil)) {
      newErrors.validUntil = 'Valid until must be after valid from';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validate() && !fileError) {
      onSave(formData);
      setFormData(initialFormData);
      setFileError(null);
    }
  };

  const handleClose = () => {
    setFormData(initialFormData);
    setErrors({});
    setFileError(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {certificateData ? 'Edit Certificate' : 'Upload Certificate'}
      </DialogTitle>
      <DialogContent>
        <Grid2 container spacing={2} sx={{ mt: 1 }}>
          <Grid2 size={12}>
            <TextField
              fullWidth
              label="Certificate Name"
              value={formData.name}
              onChange={handleChange('name')}
              error={!!errors.name}
              helperText={errors.name}
              required
            />
          </Grid2>
          <Grid2 size={12}>
            <FormControl fullWidth error={!!errors.type} required>
              <InputLabel>Certificate Type</InputLabel>
              <Select
                value={formData.type}
                label="Certificate Type"
                onChange={handleSelectChange('type')}
              >
                {certificateManagementConfig.certificateTypes.map(type => (
                  <MenuItem key={type.value} value={type.value}>
                    {type.label}
                  </MenuItem>
                ))}
              </Select>
              {errors.type && (
                <Typography variant="caption" color="error" sx={{ mt: 0.5, ml: 2 }}>
                  {errors.type}
                </Typography>
              )}
            </FormControl>
          </Grid2>
          <Grid2 size={12}>
            <TextField
              fullWidth
              label="BPN"
              value={formData.bpn}
              onChange={handleChange('bpn')}
              error={!!errors.bpn}
              helperText={errors.bpn}
              placeholder="BPNL..."
              required
            />
          </Grid2>
          <Grid2 size={12}>
            <TextField
              fullWidth
              label="Issuer"
              value={formData.issuer}
              onChange={handleChange('issuer')}
              error={!!errors.issuer}
              helperText={errors.issuer}
              required
            />
          </Grid2>
          <Grid2 size={6}>
            <TextField
              fullWidth
              type="date"
              label="Valid From"
              value={formData.validFrom}
              onChange={handleChange('validFrom')}
              error={!!errors.validFrom}
              helperText={errors.validFrom}
              InputLabelProps={{ shrink: true }}
              required
            />
          </Grid2>
          <Grid2 size={6}>
            <TextField
              fullWidth
              type="date"
              label="Valid Until"
              value={formData.validUntil}
              onChange={handleChange('validUntil')}
              error={!!errors.validUntil}
              helperText={errors.validUntil}
              InputLabelProps={{ shrink: true }}
              required
            />
          </Grid2>
          <Grid2 size={12}>
            <TextField
              fullWidth
              label="Description"
              value={formData.description || ''}
              onChange={handleChange('description')}
              multiline
              rows={2}
              placeholder="Optional description of the certificate"
            />
          </Grid2>
          <Grid2 size={12}>
            <Box
              sx={{
                border: fileError ? '2px dashed #d32f2f' : '2px dashed #ccc',
                borderRadius: 2,
                p: 3,
                textAlign: 'center',
                cursor: 'pointer',
                '&:hover': { borderColor: fileError ? '#d32f2f' : '#1976d2' }
              }}
              component="label"
            >
              <input
                type="file"
                hidden
                accept=".pdf,.png,.jpg,.jpeg"
                onChange={handleFileChange}
              />
              <CloudUploadIcon sx={{ fontSize: 48, color: fileError ? '#d32f2f' : '#666', mb: 1 }} />
              <Typography variant="body2" color={fileError ? 'error' : 'textSecondary'}>
                {fileError 
                  ? fileError
                  : formData.document 
                    ? `Selected: ${formData.document.name}`
                    : 'Click to upload certificate document (PDF, PNG, JPG - max 10MB)'}
              </Typography>
            </Box>
          </Grid2>
        </Grid2>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button onClick={handleSubmit} variant="contained" color="primary">
          {certificateData ? 'Save Changes' : 'Upload'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};
