let totalAsesorias = 0;
let totalAssAc = 0;
let totalAssDes = 0;


let totalCapacitacion = 0;
let totalCapAct = 0;
let totalCapDesc = 0;


let totalSolicitudes = 0;
let totalSolAc = 0;
let totalSolDes = 0;

let totalProfesionales = 0;
let totalProAct = 0;
let totalProDesc = 0;

let totalClientes = 0;
let totalClientesAct = 0;
let totalClientesDesc = 0;

let totalAccidentes = 0;
let totalAccidentesAct = 0;
let totalAccidentesDesc = 0;



(function () {
    'use strict'
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl)
    })
})()

$.ajax({
    url : all,
    context : document.body
}).done(function(data){
    
    /* Iterando sobre la matriz de objetos 
        y contando la cantidad de objetos que tienen 
        un estado de 1. */
    $.each(data.asesorias, function (v, e) { 
        totalAsesorias = totalAsesorias + 1;
        if (e.status == 1 ) {
            totalAssAc = totalAssAc + 1;
        } else {
            totalAssDes = totalAssDes + 1;
        }
    });

    porcentajeAsesoriasAc = (totalAssAc / totalAsesorias) * 100;
    porcentajeAsesoriasDes = (totalAssDes / totalAsesorias) * 100;
    $('#countAsesorias').html(totalAssAc);
    $('#progressBarAsesoriasElement').cs


    $.each(data.solicitudes, function (v, e) { 
        totalSolicitudes = totalSolicitudes + 1;
        if (e.status == 1 ) {
            totalSolAc = totalSolAc + 1;
        } else {
            totalSolDes =totalSolDes + 1;
        }
    });
    $('#countSolicitudes').html(totalSolAc);


    
    $.each(data.capacitaciones, function (v, e) {
        totalCapacitacion = totalCapacitacion + 1; 
        if (e.status == 1 ) {
            totalCapAct = totalCapAct + 1;
        } else {
            totalCapDesc = totalCapDesc + 1;
        }
    });
    // $('#countCapacitaciones').html(totalCapacitacion);
    $('#countCapacitacionesAct').html(totalCapAct);
    $('#countCapacitacionesDesc').html(totalCapDesc);



    $.each(data.profesionales, function (v, e) {
        totalProfesionales = totalProfesionales + 1; 
        if (e.status == 1 ) {
            totalProAct = totalProAct + 1;
        } else {
            totalProDesc = totalProDesc + 1;
        }
    });
    $('#countProfesionales').html(totalProfesionales);
    // $('#countcountProfesionalesAct').html(totalProAct);
    // $('#countcountProfesionalesDesc').html(totalProDesc);



    /* A jQuery function that iterates over an array and executes a function for each element. */
    $.each(data.clientes, function (k, e) {
        totalClientes = totalClientes + 1;

        if (e.status_cliente == 1) {
            totalClientesAct = totalClientesAct + 1;
        } else {
            totalClientesDesc = totalClientesDesc + 1;
        }
    });
    $('#countClientesAct').html(totalClientesAct);
    $('#totalClientes').html(totalClientes);
    porcentajeClientesAct = (totalClientesAct / totalClientes) * 100;
    $('#progressBarCliente').css('width', porcentajeClientesAct + '%');

    // Accidentes Reportados
    $.each(data.accidentes, function (k, e) {
        totalAccidentes = totalAccidentes + 1;

        if (e.status_accidente == 1) {
            totalAccidentesAct = totalAccidentesAct + 1;
        } else {
            totalAccidentesDesc = totalAccidentesDesc + 1;
        }
    });
    $('#countAccidentesAct').html(totalAccidentesAct);
    $('#totalAccidentes').html(totalAccidentes);
    porcentajeAccidentesAct = (totalAccidentesAct / totalAccidentes) * 100;
    $('#progressBarAccidentes').css('width', porcentajeAccidentesAct + '%');

})
