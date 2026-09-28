package com.example.clinical_documentation.service;

import com.example.clinical_documentation.entity.SoapNote;
import com.example.clinical_documentation.repository.SoapNoteRepository;

import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SoapNoteService {

    private final SoapNoteRepository repository;

    public SoapNoteService(SoapNoteRepository repository) {
        this.repository = repository;
    }

    public SoapNote saveSoapNote(SoapNote soapNote) {
        return repository.save(soapNote);
    }

    public List<SoapNote> getAllSoapNotes() {
        return repository.findAll();
    }

    public SoapNote getSoapNoteById(Long id) {
        return repository.findById(id).orElse(null);
    }
}