package com.example.clinical_documentation.controller;

import com.example.clinical_documentation.entity.SoapNote;
import com.example.clinical_documentation.service.SoapNoteService;

import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/soap-notes")
public class SoapNoteController {

    private final SoapNoteService service;

    public SoapNoteController(SoapNoteService service) {
        this.service = service;
    }

    @PostMapping
    public SoapNote saveSoapNote(@RequestBody SoapNote soapNote) {
        return service.saveSoapNote(soapNote);
    }

    @GetMapping
    public List<SoapNote> getAllSoapNotes() {
        return service.getAllSoapNotes();
    }

    @GetMapping("/{id}")
    public SoapNote getSoapNoteById(@PathVariable Long id) {
        return service.getSoapNoteById(id);
    }
}